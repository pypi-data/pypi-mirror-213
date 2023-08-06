from kaiju_tools.fixtures import BaseFixtureService

from kaiju_tasks.interface import TaskService

__all__ = ['TaskFixtureService']


class TaskFixtureService(BaseFixtureService):
    """Base user fixture service."""

    subdir = 'tasks'

    def __init__(
        self,
        task_service: TaskService = None,
        app=None,
        base_dir=BaseFixtureService.BASE_DIR,
        logger=None,
    ):
        """Initialize.

        :param task_service:
        :param app:
        :param base_dir:
        :param logger:
        """
        BaseFixtureService.__init__(self, app=app, base_dir=base_dir, logger=logger)
        self._service = task_service

    async def init(self):
        self._service = self.discover_service(name=self._service, cls=TaskService)
        await self.load_tasks()

    async def load_tasks(self) -> None:
        """Load predefined tasks from fixtures."""
        path = self._base_dir / self.subdir
        data = await self._service.list(limit=1, count=False)
        if data['data']:
            return
        for fp in path.glob('*.json'):
            data = self.load_file(fp)
            if data:
                self.logger.debug('Adding %d new tasks from %s.', len(data), fp)
                await self._service.m_create(data, columns=None)
