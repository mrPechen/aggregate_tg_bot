from pydantic import BaseModel, field_validator
from datetime import datetime


class InputData(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: str

    @field_validator("group_type")
    @classmethod
    def validate_group_type(cls, value):
        allowed_values = ["hour", "day", "month"]
        if value not in allowed_values:
            raise ValueError('Допустимо отправлять только следующие запросы:\n'
                             '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}\n'
                             '{"dt_from": "2022-10-01T00:00:00", "dt_upto": "2022-11-30T23:59:00", "group_type": "day"}\n'
                             '{"dt_from": "2022-02-01T00:00:00", "dt_upto": "2022-02-02T00:00:00", "group_type": "hour"}'
                             )
        return value

    @field_validator("*")
    @classmethod
    def check_fields_name(cls, value, field):
        expected_fields = ["dt_from", "dt_upto", "group_type"]
        if field.field_name not in expected_fields:
            raise ValueError('Невалидный запос. Пример запроса:\n'
                             '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}')
        return value
