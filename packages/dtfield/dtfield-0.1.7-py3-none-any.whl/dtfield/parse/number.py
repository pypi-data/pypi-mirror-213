__all__ = ['parse_int', 'parse_float', 'parse_decimal']

import re
from typing import Any
from decimal import Decimal
import datetime


def parse_int(value: Any) -> int:
    if isinstance(value, str):
        return int(float(re.sub(r',', '.', value)).__round__(0))
    elif isinstance(value, float):
        return int(value)
    elif isinstance(value, (datetime.datetime, datetime.date)):
        return value.toordinal()
    elif isinstance(value, bool):
        return int(value)
    return value


def parse_float(value: Any) -> float:
    if isinstance(value, str):
        return float(re.sub(r',', '.', value)).__round__(2)
    elif isinstance(value, int):
        return float(value)
    elif isinstance(value, (datetime.datetime, datetime.date)):
        return float(value.toordinal())
    elif isinstance(value, bool):
        return float(value)
    return value

def parse_decimal(value: Any) -> Decimal:
    if isinstance(value, str):
        return Decimal(re.sub(r',', '.', value))
    elif isinstance(value, int):
        return Decimal(str(float(value)))
    elif isinstance(value, (datetime.datetime, datetime.date)):
        return Decimal(value.toordinal())
    elif isinstance(value, bool):
        return Decimal(value)
    return value