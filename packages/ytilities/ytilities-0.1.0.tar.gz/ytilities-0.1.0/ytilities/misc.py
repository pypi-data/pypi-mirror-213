"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from typing import Union

from .classes import is_class, is_initialized
from .lists import listify


# pick values from list/dict/tuple/class or set
def pick(obj, keys: list, sort_keys: bool = True) -> Union[dict, list, tuple, set]:
    """Returns a subset of items from a class, dict, list, tuple or set\
          based on their keys/props.

    Args:
        obj (class, dict, list, tuple, set): value to pick items from
        keys (list): keys/props to pick
        sort_keys (bool, optional): sort picked keys/props before returning?.\
              Defaults to True.

    Raises:
        TypeError: if obj is not one of class, dict, list, tuple or set

    Returns:
        (dict, list, tuple, set): items picked from class, dict, list, tuple or set
    """
    if not isinstance(obj, (dict, list, tuple, set)) and not is_initialized(obj):
        raise TypeError(
            "obj must be a dict, list, tuple, set or an initialized class object"
        )
    if not isinstance(keys, (tuple, set, list, str, int)):
        raise TypeError("keys to pick must be a string, integer, set, tuple or list")

    keys = listify(keys)

    if sort_keys:
        keys = sorted(keys)

    if isinstance(obj, dict):
        return {k: obj[k] for k in keys if k in obj}

    elif isinstance(obj, tuple):
        length = len(obj)
        return tuple([obj[k] for k in keys if k <= length - 1])

    elif isinstance(obj, set):
        return {k for k in keys if k in obj}

    elif is_class(obj):
        return {k: getattr(obj, k) for k in keys if hasattr(obj, str(k))}

    else:
        length = len(obj)
        return [obj[k] for k in keys if k <= length - 1]
