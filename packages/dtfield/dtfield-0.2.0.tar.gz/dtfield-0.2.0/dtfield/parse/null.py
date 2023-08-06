__all__ = ['is_null']

from typing import Any
from dataclasses import MISSING


def is_null(value: Any) -> bool:
    return True if any([
            value is None,
            value == '',
            value == b'',
            value == [],
            value == {},
            value == dict(),
            value == MISSING
    ]) else False
    