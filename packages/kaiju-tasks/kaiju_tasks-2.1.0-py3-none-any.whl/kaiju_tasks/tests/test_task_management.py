from types import SimpleNamespace
from time import time

import pytest

from kaiju_tasks.etc import TaskStatus, RestartPolicy
from kaiju_tools.jsonschema import Object, compile_schema
from kaiju_tools.tests.fixtures import *
from kaiju_tools.scheduler import Scheduler
from kaiju_db.tests.fixtures import *
from kaiju_redis.tests.fixtures import *

from ..services import *


class TestService(Service, AbstractRPCCompatible):
    """Basic service."""

    service_name = 'test'

    @property
    def routes(self):
        return {'do': self.do, 'err': self.err}

    async def do(self, a: int, b: int):
        return a + b

    async def err(self):
        raise ValueError()


@pytest.fixture
def task_manager(application, redis_listener, database_service, logger) -> TaskManager:
    app = application()
    app.services = SimpleNamespace(initialized=asyncio.Event())
    app.services.initialized.set()
    app.logger = logger
    redis_listener.topics = ['rpc']
    redis_listener._locks_service_name._scheduler = scheduler = Scheduler(app=app, logger=logger)
    database_service.app = redis_listener.app = app
    app.get_session = redis_listener._rpc_service_name.get_session
    notification_service = NotificationService(app=redis_listener.app, database_service=database_service)
    task_service = TaskService(app=app, database_service=database_service)
    task_service._validator = compile_schema(Object({}, additionalProperties=True))
    manager = TaskManager(
        app=redis_listener.app,
        database_service=database_service,
        stream_service=redis_listener,
        redis_transport=redis_listener._transport_name,  # noqa
        notification_service=notification_service,
        scheduler_service=scheduler,
    )
    manager._tasks = task_service
    rpc = redis_listener._rpc_service_name  # noqa
    rpc.register_service(manager.service_name, manager)
    return manager


@pytest.mark.asyncio
@pytest.mark.docker
async def test_manager_notifications_and_cleanup(per_session_database, per_session_redis, task_manager, logger):
    task_manager.app.name = 'pytest'
    task_service = task_manager._tasks
    new_task = str(uuid.uuid4())
    executor_id = uuid.uuid4()
    async with task_manager._db:
        async with task_manager._stream:
            async with task_manager._stream._locks:
                async with task_manager:
                    await task_service.create({'id': new_task, 'commands': [{'method': 'do'}], 'notify': True})
                    await task_manager._queue_tasks()
                    await task_manager.execute_stage(new_task, executor_id, 0)
                    await task_manager.write_stage(new_task, executor_id, 0, 1, 42, False)
                    # notifications = await task_manager._notifications.list(conditions={'task_id': new_task})
                    # logger.info(notifications)
                    # assert notifications['data'][0]['result'] == [42]

                    # testing cleanup

                    # await task_manager.delete_old_tasks_and_notifications(days=0)
                    # notifications = await task_manager._notifications.list(conditions={'task_id': new_task})
                    # assert len(notifications['data']) == 0
                    # tasks = await task_service.list(conditions={'id': new_task})
                    # assert len(tasks['data']) == 0


@pytest.mark.asyncio
@pytest.mark.docker
async def test_manager_executor_management(per_session_database, per_session_redis, task_manager, logger):
    task_manager.app.name = 'pytest'
    task_service = task_manager._tasks
    new_task = str(uuid.uuid4())
    new_executor = uuid.uuid4()
    async with task_manager._db:
        async with task_manager:

            # registering executors

            await task_manager.ping(new_executor)
            active = await task_manager.list_active_executors()
            assert str(new_executor).encode('utf-8') in active
            await task_service.create({'id': new_task, 'commands': [{'method': 'do'}]})
            await task_service.update(new_task, {'executor_id': new_executor, 'status': TaskStatus.EXECUTED.value})

            # suspending executors

            await task_manager.suspend_executor(new_executor)
            active = await task_manager.list_active_executors()
            assert str(new_executor).encode('utf-8') not in active
            task = await task_service.get(new_task)
            assert task['status'] == TaskStatus.SUSPENDED.value
            assert task['executor_id'] is None

            # expelling old executors

            await task_manager.ping(new_executor)
            await task_service.update(new_task, {'executor_id': new_executor, 'status': TaskStatus.EXECUTED.value})
            await task_manager._redis.hset(task_manager.executor_map_key, {str(new_executor): 1})
            await task_manager._expell_dead_executors()
            active = await task_manager.list_active_executors()
            assert str(new_executor).encode('utf-8') not in active
            task = await task_service.get(new_task)
            assert task['status'] == TaskStatus.SUSPENDED.value
            assert task['executor_id'] is None


@pytest.mark.asyncio
@pytest.mark.docker
@pytest.mark.parametrize(
    ['data', 'after_queue'],
    [
        ({'status': TaskStatus.IDLE.value}, {'status': TaskStatus.QUEUED.value}),
        ({'status': TaskStatus.IDLE.value, 'next_run': int(time()) + 1000}, {'status': TaskStatus.IDLE.value}),
        ({'status': TaskStatus.IDLE.value, 'active': False}, {'status': TaskStatus.IDLE.value}),
        ({'status': TaskStatus.QUEUED.value, 'queued_at': time() - 1000}, {'status': TaskStatus.FAILED.value}),
        (
            {'status': TaskStatus.SUSPENDED.value, 'stage': 1, 'result': [1], 'queued_at': int(time())},
            {'status': TaskStatus.QUEUED.value, 'stage': 1, 'result': [1]},
        ),
        (
            {'status': TaskStatus.SUSPENDED.value, 'active': False, 'queued_at': int(time())},
            {'status': TaskStatus.SUSPENDED.value},
        ),
        ({'status': TaskStatus.FAILED.value}, {'status': TaskStatus.FAILED.value}),
        (
            {'status': TaskStatus.FAILED.value, 'max_retries': 3, 'stage': 1, 'result': [1], 'queued_at': int(time())},
            {'status': TaskStatus.QUEUED.value, 'stage': 1, 'result': [1]},
        ),
        (
            {
                'status': TaskStatus.FAILED.value,
                'max_retries': 3,
                'stage': 1,
                'result': [1],
                'restart_policy': RestartPolicy.FIRST.value,
                'queued_at': int(time()),
            },
            {'status': TaskStatus.QUEUED.value, 'stage': 0, 'result': [1]},
        ),
        (
            {'status': TaskStatus.FAILED.value, 'max_retries': 3, 'active': False, 'queued_at': int(time())},
            {'status': TaskStatus.FAILED.value},
        ),
        (
            {'status': TaskStatus.FAILED.value, 'max_retries': 3, 'retries': 3, 'queued_at': int(time())},
            {'status': TaskStatus.FAILED.value},
        ),
        (
            {'status': TaskStatus.FAILED.value, 'cron': '* * * * 5', 'queued_at': int(time())},
            {'status': TaskStatus.IDLE.value},
        ),
        ({'status': TaskStatus.FINISHED.value}, {'status': TaskStatus.FINISHED.value}),
        (
            {'status': TaskStatus.FINISHED.value, 'cron': '* * * * 5', 'stage': 1, 'retries': 3, 'result': [1, 2]},
            {'status': TaskStatus.IDLE.value, 'stage': 0, 'retries': 0, 'result': []},
        ),
    ],
    ids=[
        'IDLE',
        'IDLE not ready',
        'IDLE inactive',
        'QUEUED timeout',
        'SUSPENDED',
        'SUSPENDED inactive',
        'FAILED no restarts',
        'FAILED with restart',
        'FAILED with restart from stage 0',
        'FAILED inactive',
        'FAILED no restarts left',
        'FAILED cron',
        'FINISHED',
        'FINISHED cron',
    ],
)
async def test_manager_tasks(per_session_database, per_session_redis, task_manager, logger, data, after_queue):
    task_manager.app.name = 'pytest'
    task_service = task_manager._tasks
    async with task_manager._db:
        async with task_manager._stream:
            async with task_manager._stream._locks:
                async with task_manager:
                    task = await task_service.create(
                        {'commands': [{'method': 'do'}, {'method': 'do.2'}]}, columns=['id']
                    )
                    task = await task_service.update(task['id'], data, columns='*')
                    await asyncio.sleep(1)
                    logger.info('Task before: %s', task)
                    queue = await task_manager._queue_tasks()
                    logger.info('Queue %s', queue)
                    _task = await task_service.get(task['id'])
                    logger.info('Task after: %s', _task)
                    logger.info('Expected: %s', after_queue)
                    for key, value in after_queue.items():
                        assert _task[key] == value


@pytest.mark.asyncio
@pytest.mark.docker
async def test_task_chaining(per_session_database, per_session_redis, task_manager, logger):
    task_manager.app.name = 'pytest'
    task_service = task_manager._tasks
    async with task_manager._db:
        async with task_manager._stream:
            async with task_manager._stream._locks:
                async with task_manager:
                    executor_id = uuid.uuid4()
                    next_task = await task_service.create({'commands': [{'method': 'do'}]})
                    logger.debug(next_task)
                    task = await task_service.create(
                        {'commands': [{'method': 'do'}], 'next_task': next_task['id']}, columns='*'
                    )
                    logger.debug(task)
                    await task_service.update(
                        next_task['id'], {'status': TaskStatus.FINISHED.value, 'next_run': time() + 10000}
                    )
                    await task_service.update(
                        task['id'], {'status': TaskStatus.EXECUTED.value, 'executor_id': executor_id, 'stage': 0}
                    )
                    await task_manager.write_stage(task['id'], executor_id, 0, 1, 'result', False)
                    next_task = await task_service.get(next_task['id'])
                    logger.debug(next_task)
                    assert next_task['status'] == TaskStatus.IDLE.value
                    assert next_task['next_run'] <= time()


# @pytest.mark.asyncio
# @pytest.mark.docker
# async def test_manager_executor_interaction(per_session_database, per_session_redis, task_manager, logger):
#     task_manager.app.name = 'pytest'
#     task_service = task_manager._tasks
#     simple_service = TestService(app=task_manager.app)
#     task_manager._stream._rpc_service_name.register_service(simple_service.service_name, simple_service)
#     executor = TaskExecutor(
#         app=task_manager.app,
#         rpc_service=task_manager._stream._rpc_service_name,  # noqa
#         stream_service=task_manager._stream,
#         max_parallel_tasks=2,
#     )
#     executor._rpc.register_service(executor.service_name, executor)
#     async with task_manager._db:
#         task = await task_service.create(
#             {
#                 'commands': [
#                     {'method': 'test.do', 'params': {'a': 0, 'b': 1}},
#                     {'method': 'test.do', 'params': {'a': '[KWS.const]', 'b': '[RESULT.0]'}},
#                     {'method': 'test.do', 'params': {'a': '[RESULT.1]', 'b': 1}},
#                 ],
#                 'kws': {'const': 42},
#             },
#             columns=['id'],
#         )
#         task = await task_service.update(
#             task['id'],
#             {'status': TaskStatus.SUSPENDED.value, 'stage': 1, 'result': [1], 'queued_at': int(time())},
#             columns='*',
#         )
#         logger.info('Task before: %s', task)
#         async with task_manager._stream._rpc_service_name:
#             async with task_manager._stream:
#                 async with task_manager._stream._locks:
#                     async with task_manager:
#                         for consumer in task_manager._stream._consumers.values():
#                             consumer._rpc = task_manager._stream._rpc
#                         await task_manager._queue_tasks()
#                         async with executor:
#                             await asyncio.sleep(3)
#                             task = await task_service.get(task['id'])
#                             logger.info(task)
#                             assert task['status'] == TaskStatus.FINISHED.value
#                             assert task['stage'] == 2
#                             assert task['exit_code'] == 0
#                             assert task['result'] == [1, 43, 44]  # should be resumed from the last stage
