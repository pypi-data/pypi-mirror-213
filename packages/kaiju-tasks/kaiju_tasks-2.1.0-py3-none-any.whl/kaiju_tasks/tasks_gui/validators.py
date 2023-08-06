# from croniter import croniter
# from kaiju_tools.exceptions import ValidationError
#
#
# async def cron_validator(app, key: str, value, ref, **__):
#     if value is None:
#         return
#
#     if not croniter.is_valid(value):
#         raise ValidationError('Invalid cron', data=dict(key=key, value=value, code='ValidationError.invalid_cron'))
