# import abc
#
# from babel.dates import format_datetime
# from kaiju_model.fields import StringField, BooleanField, DateTimeField, IntegerField, JSONObjectField
# from kaiju_model.grid.base import BaseHandler
# from kaiju_model.model import BaseModel
#
# from .validators import cron_validator
#
# __all__ = ('TaskEditModel', 'TaskGridModel')
#
#
# class DateTimeGridHandler(BaseHandler):
#
#     def call(self, values):
#         result = {}
#         for i in values:
#             if i["value"]:
#                 result[i["id"]] = format_datetime(i["value"], locale=self._locale)
#
#         return result
#
#
# class TaskEditModel(BaseModel, abc.ABC):
#     id = StringField(read_only=True)
#     active = BooleanField()
#     task_name = StringField()
#     description = StringField()
#     status = StringField(read_only=True)
#     exit_code = IntegerField(read_only=True)
#     user_id = StringField(read_only=True)
#     cron = StringField(field_validator=cron_validator)  # TODO: cron validator
#     status_change = DateTimeField(grid_handler=DateTimeGridHandler.__name__, read_only=True)
#     next_run = DateTimeField(grid_handler=DateTimeGridHandler.__name__)
#     last_run = DateTimeField(grid_handler=DateTimeGridHandler.__name__, read_only=True)
#     created = DateTimeField(grid_handler=DateTimeGridHandler.__name__, read_only=True)
#
#
# class TaskGridModel(BaseModel, abc.ABC):
#     id = StringField()
#     task_name = StringField()
#     status = StringField()
#     user_id = StringField()
#     active = BooleanField()
#     description = StringField()
#     cron = StringField()
#     status_change = DateTimeField(grid_handler=DateTimeGridHandler.__name__)
#     next_run = DateTimeField(grid_handler=DateTimeGridHandler.__name__)
#     last_run = DateTimeField(grid_handler=DateTimeGridHandler.__name__)
#     created = DateTimeField(grid_handler=DateTimeGridHandler.__name__)
#     commands = JSONObjectField()
#     exit_code = IntegerField()
#     result = JSONObjectField()
