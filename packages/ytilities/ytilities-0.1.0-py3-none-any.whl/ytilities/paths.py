"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from os import path

from .types import ensure_type


def path_truncate(path_str: str, max_len: int = 50) -> str:
    """Truncate a path to a given length .

    Args:
        path_str (str): Path to truncate
        max_len (int, optional): Maximum length (chars) to truncate to. Defaults to 50.

    Returns:
        str: Truncated path
    """

    # Validate arguments
    ensure_type(path_str, str, "path_str")
    ensure_type(max_len, int)

    if len(path_str) < max_len:
        return path_str

    path_arr = path_str.split(path.sep)
    arr_e = []
    arr_s = []

    arr_e.append(path_arr[-1])
    char_len = len(path_arr[-1])

    for t in path_arr[0:-1]:
        if char_len < max_len:
            arr_s.append(t)
            char_len += len(t) + 1
        else:
            break

    arr = arr_s + ["..."] + arr_e

    return path.sep.join(arr)
