"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from typing import Any, Union

import numpy as np


def listify(val: Any) -> list:
    """Convert a value into a list.

    Args:
        v (Any): your value

    Returns:
        list: list either containing your input value or value if it was already a list
    """
    if isinstance(val, (tuple, set)):
        val = list(val)
    else:
        val = val if isinstance(val, list) else [val]

    return val


def __flatten(val: Union[set, list, tuple, np.ndarray]) -> iter:
    """Flatten a nested list/set/tuple/numpy array into a single iterable .

    Args:
        val (set, list, tuple, np.ndarray)

    Raises:
        TypeError: if val is one of list/set/tuple/numpy array

    Returns:
        iter: iterabable

    Yields:
        Iterator[iter]: iterabable
    """
    if not isinstance(val, (set, list, tuple, np.ndarray)):
        raise TypeError("Function expects a list, set, tuple or numpy array")

    for i in val:
        if isinstance(i, (list, tuple, np.ndarray)):
            for j in __flatten(i):
                yield j
        else:
            yield i


def flatten(
    val: Union[set, list, tuple, np.ndarray]
) -> Union[set, list, tuple, np.ndarray]:
    """Flattens a list/set/tuple/numpy array to a 1D list/set/tuple/numpy array .

    Args:
        val (set, list, tuple, np.ndarray): your value

    Raises:
        TypeError: if val is one of list/set/tuple/numpy array

    Returns:
        Union[set, list, tuple, np.ndarray]: [description]
    """
    if not isinstance(val, (set, list, tuple, np.ndarray)):
        raise TypeError("Function expects a list, set, tuple or numpy array")

    # run __flatten
    cont = list(__flatten(val=val))

    # return same value as input
    if isinstance(val, np.ndarray):
        return np.array(cont)
    elif isinstance(val, tuple):
        return tuple(cont)
    elif isinstance(val, set):
        return set(cont)
    else:
        return cont


def chunk_arr(arr: list, n: int = 4) -> list:
    """Chunk an array into n - sized chunks .

    Args:
        arr (list): list/array to chunk
        n (int, optional): length of each chunk. Defaults to 4.

    Returns:
        list: chunked array
    """

    # validate inputs
    if not isinstance(arr, list):
        raise TypeError("Expects list, got", arr)
    if not isinstance(n, int):
        raise TypeError("Expects integer, got", n)

    return [arr[i * n : (i + 1) * n] for i in range((len(arr) + n - 1) // n)]
