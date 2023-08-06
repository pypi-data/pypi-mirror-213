import json
from django.db import models
from datetime import datetime, time as dt_time


class DatetimeJsonEncoder(json.JSONEncoder):

    def default(self, o) -> str:
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, dt_time):
            return o.strftime("%H:%M:%S")
        return super(DatetimeJsonEncoder, self).default(o)


class CharField(models.Field):

    def __init__(self, **kwargs):
        kwargs['max_length'] = kwargs.pop('max_length', 1)
        super().__init__(**kwargs)

    def db_type(self, connection):
        return 'CHAR(%s)' % self.max_length


class ConfigField(models.JSONField):

    def __init__(self, **kwargs):
        encoder = kwargs.pop('encoder', DatetimeJsonEncoder)
        super().__init__(encoder=encoder, **kwargs)
