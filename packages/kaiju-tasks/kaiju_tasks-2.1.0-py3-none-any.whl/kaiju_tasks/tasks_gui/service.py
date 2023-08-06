# from app.services.utils import offset
# from kaiju_model.grid.constructor import GridConstructor
# from kaiju_tools.exceptions import ValidationError, Conflict
#
# from kaiju_tasks.services import TaskService
# from .models import TaskGridModel, TaskEditModel
#
#
# class TaskGUIService(TaskService):
#     service_name = 'tasks'
#     columns = [
#         "id",
#         "name",
#         "description",
#         "status",
#         "commands",
#         "exit_code",
#         "result",
#         "user_id",
#         "active",
#         "cron",
#         "status_change",
#         "next_run",
#         "created"
#     ]
#
#     update_columns = {
#         'name', 'description', 'cron', 'active', 'start_from', 'exec_deadline',
#         'max_exec_timeout', 'notify', 'retries', 'retry_interval', 'next_run'
#     }
#
#     @property
#     def routes(self) -> dict:
#         return {
#             **super().routes,
#             "get": self.get,
#             "grid": self.grid,
#             "update": self.update,
#             "delete_by_name": self.delete_by_name,
#             "abort_and_restart": self.abort_and_restart
#         }
#
#     @property
#     def permissions(self):
#         return {
#             self.DEFAULT_PERMISSION: self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION
#         }
#
#     async def get(self, id, grouping=False, **kwargs):
#         if 'columns' in kwargs:
#             kwargs['columns'] = self.columns
#
#         task = await super().get(id=id, **kwargs)
#
#         if not grouping:
#             return task
#
#         task = dict(task)
#         task["task_name"] = task.pop("name")
#         task.pop("app")
#
#         async with TaskEditModel(self.app, **task) as model:
#             return model.fields
#
#     async def update(self, id, **kwargs):
#         task = await self.get(id)
#
#         task = dict(task)
#
#         if 'task_name' in kwargs:
#             kwargs["name"] = kwargs.pop("task_name")
#
#         task.update(kwargs)
#         task.pop("app", None)
#
#         async with TaskEditModel(self.app, **task) as _:
#             await super().update(id, data=kwargs)
#             return True
#
#     async def grid(self, locale, query=None, page=1, per_page=24, **_):
#         _offset = offset(page, per_page)
#
#         conditions = {}
#
#         if query:
#             conditions = [
#                 {
#                     "name": {"~": query},
#                     **conditions
#                 },
#                 {
#                     "description": {"~": query},
#                     **conditions
#                 }
#             ]
#
#         data = await self.app.services.tasks.list(
#             columns=self.columns,
#             sort=[{'desc': 'status_change'}, {'desc': 'created'}],
#             conditions=conditions,
#             offset=_offset,
#             limit=per_page,
#         )
#
#         models = [TaskGridModel(self.app, init=False, **i, task_name=i["name"]) for i in data["data"]]
#         pages = data["pages"]
#         count = data["count"]
#
#         fields = [
#             "task_name",
#             "cron",
#             "active",
#             "status",
#             "commands",
#             "exit_code",
#             "result",
#             "next_run",
#             "status_change",
#         ]
#
#         async with GridConstructor(
#                 self.app,
#                 models=models,
#                 fields=fields,
#                 locale=locale,
#         ) as gc:
#             return {
#                 "data": list(gc),
#                 "fields": fields,
#                 "pagination": {
#                     "page": page,
#                     "pages": pages,
#                 },
#                 "count": count,
#             }
#
#     async def delete_by_name(self, name):
#         data = await self.app.services.tasks.list(conditions={"name": name})
#
#         if data["count"]:
#             await super().delete(id=str(data["data"][0]["id"]))
#
#         return True
#
#     async def abort_and_restart(self, id, session):
#         try:
#             await self.abort(id, session=session)
#         except Conflict:
#             pass
#
#         return await self.restart(id, session=session)
