import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg

from kaiju_tasks.etc import TaskStatus

__all__ = ['tasks', 'create_tasks_table', 'create_notifications_table', 'notifications']


def create_notifications_table(table_name: str, tasks_table, metadata: sa.MetaData, *columns: sa.Column):
    """Get notifications table."""
    table = sa.Table(
        table_name,
        metadata,
        sa.Column('id', sa_pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('task_id', sa.ForeignKey(tasks_table.c.id, ondelete='CASCADE'), nullable=True),
        sa.Column('message', sa_pg.TEXT, nullable=True),
        sa.Column('kws', sa_pg.JSONB, nullable=True, server_default=sa.text("'{}'::jsonb")),
        sa.Column('created', sa_pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('marked', sa_pg.BOOLEAN, nullable=True, server_default=sa.text('FALSE')),
        sa.Column('author_id', sa_pg.UUID(as_uuid=True), nullable=True),
        sa.Column('user_id', sa_pg.UUID(as_uuid=True), nullable=True),
        sa.Column('job_id', sa_pg.TEXT, nullable=True),
        sa.Column('status', sa_pg.TEXT, nullable=True),
        sa.Column('result', sa_pg.JSONB, nullable=True),
        sa.Column('exit_code', sa_pg.INTEGER, nullable=True),
        sa.Column('error', sa_pg.JSONB, nullable=True),
        *columns,
    )
    sa.Index('idx_notification_timestamp', table.c.user_id, table.c.created.desc())
    return table


def create_tasks_table(table_name: str, metadata: sa.MetaData, *columns: sa.Column):
    """Get tasks table."""
    t = sa.Table(
        table_name,
        metadata,
        sa.Column('id', sa_pg.TEXT, primary_key=True),
        # executor instructions
        sa.Column('app', sa_pg.TEXT, nullable=False),
        sa.Column('commands', sa_pg.JSONB, nullable=False),
        sa.Column('kws', sa_pg.JSONB, nullable=False),
        # manager instructions
        sa.Column('active', sa_pg.BOOLEAN, nullable=False),
        sa.Column('cron', sa_pg.TEXT, nullable=True),
        sa.Column('max_exec_timeout', sa_pg.INTEGER, nullable=False),
        sa.Column('max_retries', sa_pg.INTEGER, nullable=False),
        sa.Column('restart_policy', sa_pg.TEXT, nullable=False),
        sa.Column('notify', sa_pg.BOOLEAN, nullable=False),
        sa.Column('next_task', sa.ForeignKey(f'{table_name}.id', ondelete='SET NULL'), nullable=True),
        # meta
        sa.Column('name', sa_pg.TEXT, nullable=True),
        sa.Column('description', sa_pg.TEXT, nullable=True),
        sa.Column('meta', sa_pg.JSONB, nullable=False),
        # managed
        sa.Column('status', sa_pg.TEXT, nullable=False),
        sa.Column('result', sa_pg.JSONB, nullable=False),
        sa.Column('stage', sa_pg.INTEGER, nullable=False),
        sa.Column('stages', sa_pg.INTEGER, nullable=False),
        sa.Column('created', sa_pg.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('queued_at', sa_pg.INTEGER, nullable=True),
        sa.Column('exec_deadline', sa_pg.INTEGER, nullable=True),
        sa.Column('next_run', sa_pg.INTEGER, nullable=True),
        sa.Column('user_id', sa_pg.UUID(as_uuid=True), nullable=True),
        sa.Column('executor_id', sa_pg.UUID(as_uuid=True), nullable=True),
        sa.Column('job_id', sa_pg.TEXT, nullable=True),
        sa.Column('retries', sa_pg.INTEGER, nullable=False),
        sa.Column('exit_code', sa_pg.INTEGER, nullable=True),
        sa.Column('error', sa_pg.JSONB, nullable=True),
        *columns,
    )
    sa.Index(f'idx__{t.name}__queued_at', t.c.queued_at.desc(), postgresql_where=t.c.active.is_(True))
    sa.Index(f'idx__{t.name}__next_run', t.c.next_run.desc(), postgresql_where=t.c.active.is_(True))
    sa.Index(
        f'idx__{t.name}__cron', t.c.cron, postgresql_where=sa.and_(t.c.cron.isnot(None), t.c.active.is_(True))
    )  # TODO: is_not for alchemy 1.4
    sa.Index(
        f'idx__{t.name}__status__idle',
        t.c.next_run.desc(),
        postgresql_where=sa.and_(t.c.active.is_(True), t.c.status == TaskStatus.IDLE.value),
    )
    return t


tasks = create_tasks_table('tasks', sa.MetaData())
notifications = create_notifications_table('notifications', tasks, sa.MetaData())
