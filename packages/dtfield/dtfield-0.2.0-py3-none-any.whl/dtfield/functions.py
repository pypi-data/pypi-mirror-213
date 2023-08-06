from __future__ import annotations

__all__ = [
        'slug',
        'normalize',
        'normalize_lower',
        'hyphen_to_underscore',
        'underscore_to_hyphen',
        'remove_extra_whitespaces',
        'underscore_text',
        'titlecase',
        'getter',
        'map_setter',
        'last',
        'first',
        'keyattr',
        'keyitem',
        'key'
    ]

import re
from typing import Any
from operator import getitem, attrgetter, itemgetter
from unidecode import unidecode


first = lambda x: getitem(x, 0)
last = lambda x: getitem(x, -1)
keyattr = attrgetter('key')
keyitem = itemgetter('key')
key = lambda x: keyitem(x) if isinstance(x, dict) else keyattr(x) if hasattr(x, 'key') else None


def map_setter(obj: dict) -> dict:
    for k, v in obj.items():
        setattr(obj, k, property(lambda obj: obj[k]))
    return obj
    

def getter(obj: Any, prop: str, default: Any = None) -> Any:
    k = (p for p in prop.strip().split('.') if p)
    value = getattr(obj, next(k), None)
    try:
        while True:
            value = getattr(value, next(k), None)
    finally:
        return value or default
    

def remove_extra_whitespaces(string: str) -> str:
    return re.sub(r'\s+', ' ', string.strip())

def normalize(string: str) -> str:
    return unidecode(string.strip())

def normalize_lower(string: str) -> str:
    return normalize(string).lower()

def separate_words(string: str) -> str:
    def analyse_low_up(value: str):
        result = re.search(r'([a-z][A-Z])', value)
        if result:
            mid = result.span()[0] + 1
            return analyse_low_up(value[:mid] + ' ' + value[mid:])
        return value
    
    def analyse_up_up_low(value: str):
        result = re.search(r'([A-Z][A-Z][a-z])', value)
        if result:
            mid = result.span()[-1] - 2
            return analyse_up_up_low(value[:mid] + ' ' + value[mid:])
        return value
    
    return remove_extra_whitespaces(analyse_up_up_low(analyse_low_up(string)))

def underscore_text(string: str):
    return re.sub(r'\s+|-+', '_', separate_words(string))


def slug(string: str) -> str:
    return normalize_lower(underscore_text(string))


def underscore_to_hyphen(string: str) -> str:
    return re.sub(r'_+', '-', string.strip())

def hyphen_to_underscore(string: str) -> str:
    return re.sub(r'-+', '_', string.strip())


def titlecase(string: str) -> str:
    return ' '.join([w.title() if not w.isupper() and not len(w) <=2 else w for w in separate_words(string).split()])