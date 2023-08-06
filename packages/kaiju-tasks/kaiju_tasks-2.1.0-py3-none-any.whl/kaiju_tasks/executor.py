import asyncio

from kaiju_tools.exceptions import InternalError
from kaiju_tools.rpc import JSONRPCServer, AbstractRPCCompatible
from kaiju_tools.rpc.jsonrpc import RPCError
from kaiju_tools.rpc.etc import JSONRPCHeaders
from kaiju_tools.services import ContextableService
from kaiju_tools.streams import Listener, Topics
from kaiju_tools.templates import Template
from kaiju_tools.functions import retry

from .etc import TemplateKey, Limit, ExecutorTask
from .manager import TaskManager

__all__ = ['TaskExecutor']


class TaskExecutor(ContextableService, AbstractRPCCompatible):
    """Task executor receives and processes tasks from a manager."""

    service_name = 'executor'

    def __init__(
        self,
        app,
        manager_namespace: str = None,
        manager_topic: str = Topics.rpc,
        executor_topic: str = Topics.rpc,
        rpc_service: JSONRPCServer = None,
        stream_service: Listener = None,
        max_parallel_tasks: int = 4,
        logger=None,
    ):
        """Initialize.

        :param app: web app
        :param manager_namespace: namespace (app name) for a task manager
            by default will use the same as the local app name
        :param manager_topic: optional custom task manager topic name
        :param executor_topic: used to lock reads when tasks are processed
        :param rpc_service: local rpc server name or instance
        :param stream_service: listener instance
        :param max_parallel_tasks: max parallel running tasks by this executor
        :param logger: optional logger instance
        """
        ContextableService.__init__(self, app=app, logger=logger)
        self.id = id if id else app.id
        self.manager_topic = manager_topic
        self.executor_topic = executor_topic
        self.manager_namespace = manager_namespace if manager_namespace else self.app.name
        self._rpc: JSONRPCServer = rpc_service
        self._stream: Listener = stream_service
        self._task = None
        self._closing = True
        self._counter = asyncio.Semaphore(int(max_parallel_tasks))

    @property
    def routes(self):
        return {'run_task': self.run_task}

    @property
    def permissions(self) -> dict:
        return {'*': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION}

    async def init(self):
        self._closing = False
        self._rpc = self.discover_service(self._rpc, cls=JSONRPCServer)
        self._stream = self.discover_service(self._stream, cls=Listener)
        self._task = asyncio.ensure_future(self._loop())

    async def close(self):
        self._closing = True
        self._task.cancel()
        self._task = None
        await self._suspend_self()

    @property
    def closed(self) -> bool:
        return self._closing

    async def run_task(self, data: ExecutorTask) -> None:
        """Run a task and callback its results to a manager."""
        stage, deadline = data['stage'], data['exec_deadline']
        self.logger.info('Acquired task', task_id=data['id'], stage=stage, deadline=deadline)
        template_data = self._get_template_data(data)
        headers = {
            JSONRPCHeaders.REQUEST_DEADLINE_HEADER: deadline,
            JSONRPCHeaders.CORRELATION_ID_HEADER: data['job_id'],
        }
        await self._alert_on_stage_execution(data, data['stage'])
        async with self._counter:
            if self._counter.locked():
                self._stream._consumers[self.executor_topic]._unlocked.clear()  # noqa TODO: lock stream when no counter
            for n, cmd in enumerate(data['commands']):
                if self._closing:
                    break
                stage = stage + n
                try:
                    cmd = Template(cmd).fill(template_data)
                    _, result = await self._rpc.call(cmd, headers, session=None)
                except Exception as exc:
                    self.logger.error('Task execution error', exc_info=exc, task_id=data['id'], stage=stage)
                    result = RPCError(id=None, error=InternalError(base_exc=exc, message='Template evaluation error'))
                    await self._write_stage_result(data, stage, error=True, result=result)
                    break
                else:
                    error, result = self._parse_result(result)
                    await self._write_stage_result(data, stage, error, result)
                    if error:
                        break
                    template_data[TemplateKey.RESULT.value][str(stage)] = result

        self._stream._consumers[self.executor_topic]._unlocked.set()  # noqa, I know

    @staticmethod
    def _get_template_data(data: ExecutorTask) -> dict:
        return {
            TemplateKey.KWS.value: data['kws'],
            TemplateKey.RESULT.value: {str(stage): data['result'][stage] for stage in range(data['stage'])},
        }

    @staticmethod
    def _parse_result(result) -> tuple:
        """Get error flag and result from rpc server response."""
        if isinstance(result, list):
            _result = []
            for r in result:
                if isinstance(r, RPCError):
                    result.append(r.repr())
                else:
                    result.append(r.result)
            return False, _result
        elif isinstance(result, RPCError):
            result = result.repr()
            return True, result
        else:
            return False, result.result

    async def _loop(self):
        while not self._closing:
            await self._send_ping()
            await asyncio.sleep(Limit.PING_INTERVAL.value)

    async def _alert_on_stage_execution(self, data: ExecutorTask, stage: int):
        self.logger.info(
            'Executing stage',
            task_id=data['id'],
            stage=stage,
            deadline=data['exec_deadline'],
        )
        await retry(
            self._stream.call,
            kws=dict(
                namespace=self.manager_namespace,
                topic=self.manager_topic,
                headers={JSONRPCHeaders.CORRELATION_ID_HEADER: data['job_id']},
                method=f'{TaskManager.service_name}.execute_stage',
                params={'id': data['id'], 'executor_id': self.app.id, 'stage': stage},
            ),
            retries=3,
            retry_timeout=1,
            logger=self.logger,
        )

    async def _write_stage_result(self, data: ExecutorTask, stage: int, error: bool, result):
        self.logger.info(
            'Writing stage result', task_id=data['id'], stage=stage, deadline=data['exec_deadline'], error=error
        )
        await retry(
            self._stream.call,
            kws=dict(
                namespace=self.manager_namespace,
                topic=self.manager_topic,
                headers={JSONRPCHeaders.CORRELATION_ID_HEADER: data['job_id']},
                method=f'{TaskManager.service_name}.write_stage',
                params={
                    'id': data['id'],
                    'executor_id': self.app.id,
                    'stage': stage,
                    'stages': data['stages'],
                    'result': result,
                    'error': error,
                },
            ),
            retries=3,
            retry_timeout=1,
            logger=self.logger,
        )

    async def _send_ping(self):
        await retry(
            self._stream.call,
            kws=dict(
                namespace=self.manager_namespace,
                topic=self.manager_topic,
                method=f'{TaskManager.service_name}.ping',
                params={'executor_id': self.app.id},
            ),
            retries=3,
            retry_timeout=1,
            logger=self.logger,
        )

    async def _suspend_self(self):
        self.logger.info('Suspending executor')
        await retry(
            self._stream.call,
            kws=dict(
                namespace=self.manager_namespace,
                topic=self.manager_topic,
                method=f'{TaskManager.service_name}.suspend_executor',
                params={'executor_id': self.app.id},
            ),
            retries=3,
            retry_timeout=1,
            logger=self.logger,
        )
