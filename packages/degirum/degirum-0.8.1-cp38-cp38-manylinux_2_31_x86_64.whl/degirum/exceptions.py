#
# exceptions.py - DeGirum Python SDK: exceptions
# Copyright DeGirum Corp. 2022
#
# Defines declarations of exceptions used by DeGirum Python SDK
#


class DegirumException(Exception):
    """
    Base type for all DeGirum exceptions.
    """


def validate_color_tuple(color):
    """Validate if color has acceptable representation.

    Args:
        color (Any): Color object to validate.

    Raises:
        DegirumException: if color is not a three-element tuple and each element is integer number.
    """

    if not isinstance(color, tuple):
        raise DegirumException(f"Given color '{color}' is not a tuple")
    if len(color) != 3:
        raise DegirumException(
            f"Given color '{color}' must have exactly three elements"
        )
    for e in color:
        if not isinstance(e, int):
            raise DegirumException(f"Given color '{color}' must have integer elements")
