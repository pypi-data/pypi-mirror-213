"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""


import re
import types
from typing import Any, Union

from .types import ensure_type


# is variable a class?
def is_class(cls) -> bool:
    """Return True if the value is a class .

    Returns:
        bool: True if class
    """
    return str(type(cls)).startswith("<class") and hasattr(cls, "__weakref__")


# check if a class is initialized
def is_initialized(cls) -> bool:
    """Returns True if the given class is initialize .

    Raises:
        TypeError: if cls argument is not a class

    Returns:
        bool: True if class has been initialized
    """

    if not is_class(cls):
        raise TypeError("Expects a valid class, got", cls)

    new_cls = types.new_class("_")
    return is_class(cls) and type(cls) != type(new_cls)


# get properties of this class
def get_props(
    cls, filter_callable: bool = False, with_meta: bool = False
) -> Union[list, dict]:
    """List all (non default) properties of a class .

    Args:
        cls (Any): a valid class
        filter_callable (bool, optional): if True, only callable properties of\
            the class are returned. Defaults to False.
        with_meta (bool, optional): if True, a dict of properties and metadata\
        about them is returned. Defaults to False.

    Returns:
        list|dict: list or dict of properties of the class
    """

    # validate inputs
    if not is_class:
        raise TypeError("Expects 'cls' to be a class, got", cls)

    ensure_type(filter_callable, bool, "filter_callable")
    ensure_type(with_meta, bool, "with_meta")

    default_props = dir(types.new_class("_"))

    resp = {} if with_meta else set()

    for p in dir(cls):
        if p not in default_props and (
            getattr(cls, p) if not filter_callable else callable(getattr(cls, p))
        ):
            if with_meta:
                resp[p] = {
                    "type": re.match(r"<class\s+'([^>']+)", str(type(getattr(cls, p))))[
                        1
                    ],
                    "value": (
                        getattr(cls, p) if not callable(getattr(cls, p)) else "N/A"
                    ),
                }

            else:
                resp.add(p)

    return resp


def get_prop_values(
    obj: Any,
    decode_bytes: bool = True,
    run_callable: bool = False,
    skip_callable: bool = True,
) -> dict:
    """Get property values of a class/object .

    Args:
        obj (Any): the object to get properties from
        decode_bytes (bool, optional): try and decode any byte values\
              to utf-8. Defaults to True.
        run_callable (bool, optional): try and run callable properties.\
              Defaults to False.
        skip_callable (bool, optional): determines if to include callable\
              values in response. Defaults to True.

    Returns:
        dict: a dict of {property:value} pairs
    """

    # validate inputs
    ensure_type(decode_bytes, bool, "decode_bytes")
    ensure_type(run_callable, bool, "run_callable")
    ensure_type(skip_callable, bool, "skip_callable")

    prop_vals = {}
    for p in dir(obj):
        val = getattr(obj, p)

        if decode_bytes and isinstance(val, bytes):
            try:
                val = val.decode()
            except UnicodeError:
                pass

        if callable(val):
            if run_callable:
                try:
                    val = val()
                except Exception as e:
                    val = e.args[0]
                    pass

            if not skip_callable:
                prop_vals[p] = val

        else:
            prop_vals[p] = val

    return prop_vals
