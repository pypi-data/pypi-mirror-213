"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

import re
from typing import Any

from .lists import listify

types_obj = {
    "int": "integer",
    "float": "float",
    "complex": "complex",
    "str": "string",
    "list": "list",
    "tuple": "tuple",
    "range": "range",
    "bytes": "bytes",
    "bytearray": "bytearray",
    "memoryview": "memoryview",
    "dict": "dict",
    "bool": "boolean",
    "set": "set",
    "frozenset": "frozenset",
    "NoneType": "NoneType",
}


def get_type_name(_type) -> str:
    """Return the type name of a Python object. \
        This returns full names for types so that str=>"string" and so on...

    Args:
        _type (type): the type you want to get the name of. \
            Example get_type_name(str) -> "string"

    Returns:
        str: full name of the type
    """
    groups = re.search(r"<class\s+'([^']+)'", str(_type)).groups()

    return types_obj[groups[0]]


def ensure_type(val: Any, _types, val_name: str = None) -> None:
    """Ensure that value is of a valid type .

    Args:
        val (Any): value you want to ensure type for
        _types (type, tuple(type)): the data types you want to validate against. \
            E.g (str,int,float)
        val_name (str, optional): the actual name of the variable you are validating. \
            Example `ensure_type(var_1, (int, float), 'var_1'). Defaults to None.

    Raises:
        TypeError: if value does not match the validation types entered
    """
    _types = tuple(listify(_types))

    for _type in _types:
        if not type(type) == type(_type):
            raise TypeError("Expects '_type' to be a valid type, got", _type)

    # validate arguments
    if val_name and not isinstance(val_name, str):
        raise TypeError("Expects 'val_name' to be a string, got", val_name)

    if not isinstance(val, _types):
        val_name_str = f" '{val_name}' to be" if val_name else ""
        types_str = [get_type_name(_type) for _type in _types]
        types_str = ", ".join(types_str)

        raise TypeError(f"Expects{val_name_str} '{types_str}', got", val)
