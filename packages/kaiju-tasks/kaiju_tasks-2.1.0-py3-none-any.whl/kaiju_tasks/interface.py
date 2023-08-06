import time
import uuid
from datetime import datetime, timedelta

import sqlalchemy as sa  # noqa pycharm
from croniter import croniter  # noqa pycharm

import kaiju_tools.jsonschema as j
from kaiju_db.services import SQLService
from kaiju_tools.exceptions import ValidationError
from kaiju_tools.rpc import AbstractRPCCompatible

from .etc import Permission, TaskStatus, Task, RestartPolicy, Limit
from .tables import tasks

__all__ = ['TaskService', 'task_schema']


task_command = j.Object(
    {'id': j.Integer(), 'method': j.String(), 'params': j.Object()}, additionalProperties=False, required=['method']
)


task_schema = j.Object(
    {
        'id': j.String(minLength=1),
        'app': j.String(),
        'commands': j.Array(task_command, minItems=1, maxItems=Limit.MAX_STAGES.value),
        'kws': j.Object(),
        'cron': j.String(),
        'max_exec_timeout': j.Integer(minimum=Limit.MIN_T.value, maximum=Limit.MAX_T.value),
        'max_retries': j.Integer(minimum=0, maximum=Limit.MAX_RETRIES.value),
        'restart_policy': j.Enumerated(enum=[RestartPolicy.CURRENT.value, RestartPolicy.FIRST.value]),
        'next_task': j.String(minLength=1),
        'notify': j.Boolean(),
        'name': j.String(),
        'description': j.String(),
        'meta': j.Object(),
    },
    additionalProperties=False,
    required=[],
)


class TaskService(SQLService, AbstractRPCCompatible):
    """RPC interface for user tasks."""

    service_name = 'tasks'
    table = tasks

    def __init__(self, app, *, database_service: str = None, logger=None):
        """Initialize."""
        super().__init__(app=app, database_service=database_service, logger=logger)
        self._validator = j.compile_schema(task_schema)

    @property
    def routes(self) -> dict:
        return {**super().routes, 'restart_task': self.restart_task, 'delete_old_tasks': self.delete_old_tasks}

    @property
    def permissions(self) -> dict:
        return {
            '*': self.PermissionKeys.GLOBAL_USER_PERMISSION,
            'delete_old_tasks': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION,
        }

    async def delete_old_tasks(self, interval_days: int = 7) -> None:
        """Delete old tasks and notifications (cron tasks are excluded)."""
        sql = self.table.delete().where(
            sa.and_(self.table.c.cron.is_(None), self.table.c.created < datetime.now() - timedelta(days=interval_days))
        )
        await self._wrap_delete(None, sql)

    async def restart_task(self, task_id: str) -> None:
        """Restart a finished task."""
        data = await self.get(task_id, columns=['status', 'retries', 'max_retries'])
        status = data['status']
        if status in {TaskStatus.FINISHED, TaskStatus.FAILED}:
            sql = (
                self.table.update()
                .where(self.table.c.id == task_id)
                .values(
                    {
                        'status': TaskStatus.IDLE.value,
                        'executor_id': None,
                        'job_id': uuid.uuid4().hex[:8],
                        'exit_code': None,
                        'error': None,
                        'retries': 0,
                        'exec_deadline': None,
                        'stage': 0,
                        'result': [],
                    }
                )
            )
            await self._wrap_update(None, sql)
        else:
            raise ValueError('Task is in %s and cannot be restarted.', status)

    def prepare_insert_data(self, data: dict):
        """Prepare task."""
        data = self._validate_data(data)
        task = Task(
            id=data.get('id', str(uuid.uuid4()).replace('-', '')),
            app=data.get('app', self.app.name),
            commands=data['commands'],
            kws=data.get('kws', {}),
            cron=data.get('cron'),
            max_exec_timeout=data.get('max_exec_timeout', Limit.DEFAULT_T.value),
            max_retries=data.get('max_retries', 0),
            name=data.get('name'),
            description=data.get('description'),
            meta=data.get('meta', {}),
            notify=data.get('notify', False),
            restart_policy=data.get('restart_policy', RestartPolicy.CURRENT.value),
            active=True,
            status=TaskStatus.IDLE.value,
            stage=0,
            stages=len(data['commands']),
            result=[],
            created=sa.func.now(),
            queued_at=None,
            exec_deadline=None,
            next_run=int(time.time()),
            user_id=self.get_user_id(),
            executor_id=None,
            job_id=uuid.uuid4().hex[:8],
            retries=0,
            exit_code=None,
            error=None,
            next_task=data.get('next_task'),
        )
        return task

    def prepare_update_data(self, data: dict):
        return self._validate_data(data)

    def _validate_data(self, data: dict) -> dict:
        data = self._validator(data)
        cron = data.get('cron')
        if cron:
            croniter(data.get('cron'), start_time=datetime.now()).next()  # testing for validity
        commands = data.get('commands')
        if commands and len(commands) == 0:
            raise ValidationError('Commands must not be empty.')
        return data

    def _set_user_condition(self, sql, permission):
        """Places user condition if a user has no admin/system privileges."""
        if self.has_permission(permission):
            user_id = self.get_user_id()
            sql = sql.where(self.table.c.user_id == user_id)
        return sql

    def _get_condition_hook(self, sql):
        return self._set_user_condition(sql, Permission.VIEW_OTHERS_TASKS.value)

    def _update_condition_hook(self, sql):
        return self._set_user_condition(sql, Permission.MODIFY_OTHERS_TASKS.value)

    def _delete_condition_hook(self, sql):
        return self._update_condition_hook(sql)
