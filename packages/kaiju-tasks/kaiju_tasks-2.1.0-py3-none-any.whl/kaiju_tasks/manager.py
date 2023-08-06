import uuid
from datetime import datetime, timezone, timedelta
from time import time
from typing import Any, List

import sqlalchemy as sa  # noqa pycharm
from croniter import croniter  # noqa pycharm

from kaiju_db.services import DatabaseService
from kaiju_redis import RedisTransportService
from kaiju_tools.streams import Listener, Topics
from kaiju_tools.rpc import AbstractRPCCompatible
from kaiju_tools.rpc.etc import JSONRPCHeaders
from kaiju_tools.services import ContextableService
from kaiju_tools.scheduler import Scheduler

from .etc import Task, TaskStatus, RestartPolicy, Notification, Limit, ExecutorTask, ExitCode
from .notifications import NotificationService
from .tables import tasks

__all__ = ['TaskManager']


class TaskManager(ContextableService, AbstractRPCCompatible):
    """Task manager schedules tasks execution."""

    service_name = 'taskman'
    table = tasks

    def __init__(
        self,
        app,
        database_service: DatabaseService = None,
        stream_service: Listener = None,
        redis_transport: RedisTransportService = None,
        notification_service: NotificationService = None,
        scheduler_service: Scheduler = None,
        executor_topic: str = Topics.rpc,
        refresh_rate: int = 1,
        suspended_task_lifetime_hours: int = 24,
        logger=None,
    ):
        """Initialize.

        :param app: web app
        :param database_service: database connector instance or service name
        :param stream_service: stream service (Listener) for sending rpc queries
        :param redis_transport: a cache for executor states\
        :param notification_service: notification service instance or service name
        :param scheduler_service: internal loop scheduler
        :param refresh_rate: watcher loop refresh rate in seconds
        :param executor_topic: optional topic name for executor
        :param suspended_task_lifetime_hours: if task was last queued before this interval, it won't be executed again
        :param logger: optional logger
        """
        super().__init__(app=app, logger=logger)
        self._db = self.discover_service(database_service, cls=DatabaseService)
        self._scheduler = scheduler_service
        self._stream = stream_service
        self._notifications = notification_service
        self._redis = redis_transport
        self._refresh_interval = max(1, int(refresh_rate))
        self._suspended_lifetime = max(1, int(suspended_task_lifetime_hours))
        self._executor_topic = executor_topic
        self.executor_map_key = f'{self.service_name}.executors'
        self._task = None
        self._closing = None

    @property
    def routes(self) -> dict:
        return {
            'list_active_executors': self.list_active_executors,
            'ping': self.ping,
            'suspend_executor': self.suspend_executor,
            'execute_stage': self.execute_stage,
            'write_stage': self.write_stage,
            'cleanup': self.cleanup,
        }

    @property
    def permissions(self) -> dict:
        return {'*': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION}

    async def init(self):
        self._closing = False
        self._scheduler: Scheduler = self.discover_service(self._scheduler, cls=Scheduler)
        self._notifications = self.discover_service(self._notifications, cls=NotificationService)
        self._redis = self.discover_service(self._redis, cls=RedisTransportService)
        self._stream = self.discover_service(self._stream, cls=Listener)
        self._task = self._scheduler.schedule_task(
            self._queue_tasks, interval=self._refresh_interval, policy=Scheduler.ExecPolicy.WAIT, name='taskman.loop'
        )

    async def close(self):
        self._task.enabled = False

    @property
    def closed(self) -> bool:
        return self._closing is None

    async def list_active_executors(self) -> dict:
        """Return executor ids and their last ping time."""
        return await self._redis.hgetall(self.executor_map_key)

    async def cleanup(self, task_lifetime: int, notifications_lifetime: int) -> None:
        """Remove old unused tasks and notifications.

        Non-periodic tasks which have reached lifetime limit will be removed. All notifications related to them will
        also be removed.

        All notifications (incl. for periodic tasks) which have reached `notifications_lifetime` will be also removed.
        """
        t = datetime.now() - timedelta(seconds=task_lifetime)
        sql = self.table.delete().where(sa.and_(self.table.c.cron.is_(None), self.table.c.created < t))
        await self._db.execute(sql)
        t = datetime.now() - timedelta(seconds=notifications_lifetime)
        await self._notifications.m_delete(conditions={'created': {'lt': t}})

    async def ping(self, executor_id: uuid.UUID) -> None:
        """Ping the manager to tell that you're ok."""
        await self._redis.hset(self.executor_map_key, {str(executor_id): int(time())})

    async def suspend_executor(self, executor_id: uuid.UUID) -> None:
        """Suspend an executor and its tasks."""
        self.logger.debug('Suspending executor (requested)', executor_id=executor_id)
        sql = (
            self.table.update()
            .where(sa.and_(self.table.c.status == TaskStatus.EXECUTED.value, self.table.c.executor_id == executor_id))
            .values({'status': TaskStatus.SUSPENDED.value, 'executor_id': None})
        )
        await self._db.execute(sql)
        await self._redis.hdel(self.executor_map_key, [str(executor_id)])

    async def execute_stage(self, id: str, executor_id: uuid.UUID, stage: int):  # noqa id
        """Tell the manager which stage is being executed."""
        self.logger.info('Stage is executed', task_id=id, stage=stage, executor_id=executor_id)
        sql = (
            self.table.update()
            .where(sa.and_(self.table.c.id == id, self.table.c.status == TaskStatus.QUEUED.value))
            .values(
                {
                    'status': TaskStatus.EXECUTED.value,
                    # 'stage': stage,
                    'executor_id': executor_id,
                }
            )
        )
        await self._db.execute(sql)
        await self.ping(executor_id)

    async def write_stage(
        self, id: str, executor_id: uuid.UUID, stage: int, stages: int, result: Any, error: bool  # noqa id
    ):
        """Write stage result to the task table.

        This method will also change task status depending on which stage has been executed. The task my become
        'FINISHED' or 'FAILED'.
        """
        sql = self.table.update().where(
            sa.and_(
                self.table.c.id == id,
                self.table.c.executor_id == executor_id,
                self.table.c.stage == stage,
                self.table.c.status.in_([TaskStatus.EXECUTED.value, TaskStatus.QUEUED.value]),
            )
        )
        columns = [self.table.c.job_id, self.table.c.result, self.table.c.notify, self.table.c.user_id]
        if error:
            self.logger.info('Stage failed', stage=stage, task_id=id, executor_id=executor_id, error=error)
            sql = sql.values(
                {
                    'status': TaskStatus.FAILED.value,
                    'error': result,
                    'exit_code': ExitCode.EXECUTION_ERROR.value,
                    'executor_id': None,
                    'next_run': None,
                }
            ).returning(*columns)
            task = await self._db.execute(sql)
            task = task.first()
            if task and task.notify:
                task = task._asdict()  # noqa
                notification = Notification(
                    message='task.result',
                    user_id=task['user_id'],
                    task_id=id,
                    job_id=task['job_id'],
                    status=TaskStatus.FAILED.value,
                    result=task['result'],
                    exit_code=ExitCode.EXECUTION_ERROR.value,
                    error=result,
                )
                await self._notifications.create(notification, columns=[])
        elif stage == stages - 1:
            self.logger.info('Task finished', stage=stage, task_id=id, executor_id=executor_id)
            columns.append(self.table.c.next_task)
            sql = sql.values(
                {
                    'status': TaskStatus.FINISHED.value,
                    'result': self.table.c.result + [result],
                    'exit_code': ExitCode.SUCCESS.value,
                    'executor_id': None,
                    'next_run': None,
                }
            ).returning(*columns)
            task = await self._db.execute(sql)
            task = task.first()
            if task and task.next_task:
                self.logger.info('Starting next task', task_id=id, next_task=task.next_task)
                sql = (
                    self.table.update()
                    .where(
                        sa.and_(
                            self.table.c.id == task.next_task,
                            self.table.c.status.in_(
                                [TaskStatus.IDLE.value, TaskStatus.FAILED.value, TaskStatus.FINISHED.value]
                            ),
                            self.table.c.active.is_(True),
                        )
                    )
                    .values({'status': TaskStatus.IDLE.value, 'next_run': int(time())})
                )
                await self._db.execute(sql)
            if task and task.notify:
                task = task._asdict()  # noqa
                notification = Notification(
                    message='task.result',
                    user_id=task['user_id'],
                    task_id=id,
                    job_id=task['job_id'],
                    status=TaskStatus.FINISHED.value,
                    result=task['result'],
                    exit_code=ExitCode.SUCCESS.value,
                )
                await self._notifications.create(notification, columns=[])
        else:
            self.logger.info('Stage finished', stage=stage, task_id=id, executor_id=executor_id)
            sql = sql.values(
                {'status': TaskStatus.EXECUTED.value, 'result': self.table.c.result + [result], 'stage': stage + 1}
            )
            await self._db.execute(sql)

    async def _queue_tasks(self):
        await self._expell_dead_executors()
        await self._abort_timed_out_tasks()
        await self._restart_cron_tasks()
        await self._queue_suspended_and_idle()
        await self._queue_failed()

    async def _expell_dead_executors(self):
        """Check if some executors are not responding and abort their tasks."""
        dead_executors = await self._find_dead_executors()
        if dead_executors:
            sql = (
                self.table.update()
                .where(
                    sa.and_(
                        self.table.c.executor_id.in_(dead_executors), self.table.c.status == TaskStatus.EXECUTED.value
                    )
                )
                .values({'status': TaskStatus.SUSPENDED.value, 'executor_id': None})
            )
            self.logger.info('Suspending dead executors', executor_id=dead_executors)
            await self._db.execute(sql)
            await self._redis.hdel(self.executor_map_key, dead_executors)

    async def _find_dead_executors(self) -> List[str]:
        executors = await self._redis.hgetall(self.executor_map_key)
        t = time()
        dt = Limit.PING_INTERVAL.value * 4
        dead_executors = [key.decode('utf-8') for key, t0 in executors.items() if t - int(t0.decode('utf-8')) > dt]
        return dead_executors

    async def _queue_suspended_and_idle(self):
        """Queue all suspended tasks."""
        sql = (
            self.table.update()
            .where(
                sa.or_(
                    sa.and_(
                        self.table.c.status == TaskStatus.IDLE.value,
                        self.table.c.next_run < int(time()),
                        self.table.c.active.is_(True),
                    ),
                    sa.and_(
                        self.table.c.status == TaskStatus.SUSPENDED.value,
                        self.table.c.queued_at > int(time()) - self._suspended_lifetime * 3600,
                        self.table.c.active.is_(True),
                    ),
                )
            )
            .values(
                {
                    'status': TaskStatus.QUEUED.value,
                    'queued_at': int(time()),
                    'exec_deadline': int(time()) + self.table.c.max_exec_timeout,
                }
            )
            .returning(
                self.table.c.id,
                self.table.c.commands,
                self.table.c.kws,
                self.table.c.stage,
                self.table.c.exec_deadline,
                self.table.c.app,
                self.table.c.result,
                self.table.c.job_id,
            )
        )
        async with self._db.begin() as conn:
            queued_tasks = await conn.execute(sql)
            queued_tasks = [r._asdict() for r in queued_tasks.all()]  # noqa
            await self._send_tasks(queued_tasks)
            await conn.commit()

    async def _abort_timed_out_tasks(self):
        """Abort all queued tasks reached their timeout."""
        sql = (
            self.table.update()
            .where(
                sa.and_(
                    self.table.c.queued_at < int(time()) - Limit.MIN_T.value - self.table.c.max_exec_timeout,
                    self.table.c.status.in_([TaskStatus.QUEUED.value, TaskStatus.EXECUTED.value]),
                    self.table.c.active.is_(True),
                )
            )
            .values(
                {
                    'status': TaskStatus.FAILED.value,
                    'error': None,
                    'exit_code': ExitCode.ABORTED.value,
                    'next_run': None,
                }
            )
            .returning(self.table.c.id)
        )
        await self._db.execute(sql)

    async def _queue_failed(self):
        """Queue all failed tasks with available retries."""
        sql = (
            self.table.update()
            .where(
                sa.and_(
                    self.table.c.queued_at > int(time()) - self._suspended_lifetime * 3600,
                    self.table.c.status == TaskStatus.FAILED.value,
                    self.table.c.max_retries > self.table.c.retries,
                    self.table.c.active.is_(True),
                )
            )
            .values(
                {
                    'status': TaskStatus.QUEUED.value,
                    'queued_at': int(time()),
                    'exec_deadline': int(time()) + self.table.c.max_exec_timeout,
                    'stage': sa.text(
                        f"CASE WHEN {self.table.c.restart_policy.name} = '{RestartPolicy.CURRENT.value}'"
                        f' THEN {self.table.c.stage.name}'
                        ' ELSE 0 END'
                    ),  # CURRENT or FIRST
                    'executor_id': None,
                    'retries': self.table.c.retries + 1,
                    'exit_code': None,
                }
            )
            .returning(
                self.table.c.id,
                self.table.c.commands,
                self.table.c.kws,
                self.table.c.stage,
                self.table.c.exec_deadline,
                self.table.c.app,
                self.table.c.result,
                self.table.c.job_id,
            )
        )
        async with self._db.begin() as conn:
            queued_tasks = await conn.execute(sql)
            queued_tasks = [r._asdict() for r in queued_tasks.all()]  # noqa
            await self._send_tasks(queued_tasks)
            await conn.commit()

    async def _restart_cron_tasks(self):
        """Reset all finished cron tasks to IDLE."""
        t = datetime.now(timezone.utc)
        sql = (
            self.table.update()
            .where(
                sa.and_(
                    self.table.c.cron.isnot(None),
                    self.table.c.active.is_(True),
                    sa.or_(
                        self.table.c.status == TaskStatus.FINISHED.value,
                        sa.and_(
                            self.table.c.status == TaskStatus.FAILED.value,
                            self.table.c.max_retries <= self.table.c.retries,
                        ),
                    ),
                )
            )
            .values(
                {
                    'status': TaskStatus.IDLE.value,
                    'result': [],
                    'stage': 0,
                    'executor_id': None,
                    'retries': 0,
                    'exit_code': None,
                    'error': None,
                }
            )
            .returning(self.table.c.id, self.table.c.cron)
        )
        async with self._db.begin() as conn:
            cron_tasks = await conn.execute(sql)
            cron_tasks = [r._asdict() for r in cron_tasks.all()]  # noqa
            if cron_tasks:
                sql = (
                    self.table.update()
                    .where(self.table.c.id == sa.bindparam('_id'))
                    .values({'next_run': sa.bindparam('next_run'), 'job_id': sa.bindparam('job_id')})
                )
                cron_tasks = [
                    {
                        '_id': task['id'],
                        'next_run': int(croniter(task['cron'], t).next(datetime).timestamp()),
                        'job_id': uuid.uuid4().hex[:8],
                    }
                    for task in cron_tasks
                ]
                sql.__len__ = lambda: 1  # TODO: alchemy compatibility ?
                await conn.execute(sql, cron_tasks)
            await conn.commit()

    async def _send_tasks(self, queued_tasks: List[Task]):
        """Send tasks to executor streams."""
        for task in queued_tasks:
            stage = task['stage']
            await self._stream.call(
                topic=self._executor_topic,
                namespace=task['app'],
                method='executor.run_task',
                headers={JSONRPCHeaders.CORRELATION_ID_HEADER: task['job_id']},
                params={
                    'data': ExecutorTask(
                        id=task['id'],
                        commands=task['commands'][stage:],
                        kws=task['kws'],
                        result=task['result'][:stage],
                        exec_deadline=task['exec_deadline'],
                        stage=stage,
                        stages=len(task['commands']),
                        job_id=task['job_id'],
                    )
                },
            )
