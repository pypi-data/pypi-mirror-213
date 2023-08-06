__all__ = ['parse_str', 'parse_bytes']

from typing import Any
import datetime


def parse_str(value: Any) -> str:
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    elif isinstance(value, bytes):
        return value.decode('utf-8')
    elif hasattr(value, 'key'):
        return value.key
    return str(value)


def parse_bytes(value: Any) -> bytes:
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat().encode('utf-8')
    elif hasattr(value, 'key'):
        return str(value.key).encode('utf-8')
    return str(value).encode('utf-8')