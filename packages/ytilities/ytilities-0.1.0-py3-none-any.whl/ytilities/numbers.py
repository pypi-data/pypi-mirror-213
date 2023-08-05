"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""


def human_format(value) -> str:
    """Return a human - readable representation of a number .

    Args:
        value ([int,float]): Value you wish to format

    Raises:
        Exception: TypeError

    Returns:
        str: A string representing the number in easy human readable form e.g "2.345K"
    """
    if not isinstance(value, (int, float)):
        raise Exception("Integer/Float value expected")

    num = value
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0

    result = round(value / (1000**magnitude), 3)

    return "{}{}".format(result, ["", "K", "M", "B", "T"][magnitude])
