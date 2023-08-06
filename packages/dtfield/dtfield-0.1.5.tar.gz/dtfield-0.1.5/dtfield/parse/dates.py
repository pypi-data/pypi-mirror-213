__all__ = ['parse_date', 'parse_datetime']

from typing import Any
import datetime


def parse_date(value: Any) -> datetime.date:
    if type(value) is datetime.date:
        return value
    elif type(value) is datetime.datetime:
        return value.date
    elif isinstance(value, str):
        return datetime.date.fromisoformat(value)
    return value
    
    
def parse_datetime(value: Any) -> datetime.datetime:
    if type(value) is datetime.date:
        return datetime.datetime(value.year, value.month, value.date)
    elif type(value) is datetime.datetime:
        return value
    elif isinstance(value, str):
        return datetime.datetime.fromisoformat(value)
    return value