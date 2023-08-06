__all__ = [
        'T',
        'TupleOfTypes',
        'Key',
        'TableKey',
        'KeyList',
        'TableKeyList',
]

from typing import TypeVar

T = TypeVar('T')
TupleOfTypes = tuple[type]
Key = TypeVar('Key')
TableKey = TypeVar('TableKey')
KeyList = TypeVar('KeyList')
TableKeyList = TypeVar('TableKeyList')