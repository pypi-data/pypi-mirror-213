from datetime import datetime
from enum import Enum
from typing import Optional, TypedDict, Union, List
from uuid import UUID

from kaiju_db.sql_service import ErrorCodes as ErrorCodes_Base
from kaiju_tools.rpc.jsonrpc import RPCRequest

__all__ = [
    'Permission',
    'ErrorCodes',
    'TaskStatus',
    'TemplateKey',
    'Task',
    'RestartPolicy',
    'Limit',
    'Notification',
    'ExecutorTask',
    'ExitCode',
]


class TaskCommand(TypedDict, total=False):
    """Task command format."""

    method: str
    params: Optional[dict]


class ExitCode(Enum):
    """Default task exit codes."""

    SUCCESS = 0
    EXECUTION_ERROR = 1
    ABORTED = 130


class Limit(Enum):
    """Time limit constants."""

    MAX_STAGES = 100  #: max number of stages per task
    MAX_RETRIES = 10  #: max retries per job
    MIN_T = 10  #: (s) minimum acknowledged time interval in all calculations
    DEFAULT_T = 300  #: (s) default timeout
    MAX_T = 3600 * 4  #: (s) maximum allowed timeout for a single task
    PING_INTERVAL = 20  #: (s) executor ping interval


class Permission(Enum):
    """Task service user permission keys."""

    VIEW_OTHERS_TASKS = 'tasks.view_other_tasks'
    MODIFY_OTHERS_TASKS = 'tasks.modify_others_tasks'
    VIEW_OTHERS_NOTIFICATIONS = 'notifications.view_others_notifications'
    MODIFY_OTHERS_NOTIFICATIONS = 'notifications.edit_others_notifications'


class ErrorCodes(ErrorCodes_Base):
    """Task manager error codes."""

    INVALID_TASK = 'tasks.invalid_task'
    STATUS_NOT_ALLOWED = 'tasks.status_change_not_allowed'
    NOT_ACTIVE = 'tasks.not_active'
    LOCKED = 'tasks.locked'


class RestartPolicy(Enum):
    """Task manager restart policies."""

    CURRENT = 'CURRENT'  #: restart from the current stage
    FIRST = 'FIRST'  #: restart from the first stage


class TaskStatus(Enum):
    """Task manager task status list."""

    IDLE = 'IDLE'  #: initialized in the table
    QUEUED = 'QUEUED'  #: sent to an executor stream
    EXECUTED = 'EXECUTED'  #: accepted by an executor
    FINISHED = 'FINISHED'  #: all stages completed
    FAILED = 'FAILED'  #: error during stage execution
    SUSPENDED = 'SUSPENDED'  #: executor suspended, waiting for re-queuing


class TemplateKey(Enum):
    """Template keys in each executor stage."""

    KWS = 'KWS'  #: keyword args provided in Task.kws
    RESULT = 'RESULT'  #: stage results, keys starting from '0'


class Notification(TypedDict, total=False):
    """Notification data."""

    id: UUID  #: generated
    message: Optional[str]  #: human-readable message or tag
    kws: Optional[dict]  #: format keywords
    created: datetime  #: timestamp
    marked: bool  #: marked as read
    author_id: Optional[UUID]  #: sender
    user_id: Optional[UUID]  #: receiver
    task_id: Optional[str]  #: task id
    job_id: Optional[str]  #: job id
    status: Optional[str]  #: task status
    result: Optional[list]  #: results
    exit_code: Optional[int]
    error: Optional[dict]


class Task(TypedDict):
    """Task data."""

    id: str  #: generated or user-defined

    # executor instructions

    app: str  #: executor type
    commands: List[Union[TaskCommand, RPCRequest, List[TaskCommand], List[RPCRequest]]]  #: sequential list of commands
    kws: dict  #: additional kws template arguments

    # manager instructions

    active: bool  #: inactive tasks are not queued
    cron: str  #: cron instructions for periodic tasks
    max_exec_timeout: int  #: (s) max allowed execution time in total
    max_retries: int  #: max retries for a failed task (0 for no retries)
    restart_policy: str  #: how the task will be restarted
    notify: bool  #: notify user about status changes
    next_task: Optional[str]  #: next task to run after finishing of this one

    # meta

    name: Optional[str]  #: task short name
    description: Optional[str]  #: task long description
    meta: dict  #: task metadata

    # managed params

    status: str  #: current task status
    result: list  #: task execution result, a list of stage returns
    stage: int  #: current stage being executed (or about to execute)
    stages: int  #: total number of stages
    queued_at: Optional[int]  #: UNIX time last queued
    exec_deadline: Optional[int]  #: UNIX time deadline
    next_run: Optional[int]  #: UNIX time for next run
    user_id: Optional[UUID]  #: user created the task
    executor_id: Optional[UUID]  #: which executor has this task
    job_id: Optional[str]  #: updated for each new run
    retries: int  #: current number of retries
    created: datetime  #: when task record was added to the table
    exit_code: Optional[int]  #: exit (error) code similar to UNIX codes
    error: Optional[dict]  #: last error (if present)


class ExecutorTask(TypedDict):
    """Task data passed to an executor."""

    id: str
    commands: List[Union[TaskCommand, RPCRequest]]  #: sequential list of commands
    kws: dict  #: additional kws template arguments
    result: list  #: task execution result, a list of stage returns
    stage: int  #: current stage being executed (or about to execute)
    stages: int  #: total number of stages
    exec_deadline: int  #: UNIX time deadline
    job_id: str
