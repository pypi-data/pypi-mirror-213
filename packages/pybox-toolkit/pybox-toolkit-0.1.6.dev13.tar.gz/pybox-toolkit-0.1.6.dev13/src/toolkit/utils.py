"""Miscelaneous utilities for the toolkit"""

from math import copysign, isnan
from collections.abc import Iterable
from typing import Callable
from typing_extensions import TypeVar

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")

class ToolkitException(Exception):
    """Base class for exceptions in the toolkit."""


class RangeException(ToolkitException):
    """Exception raised for invalid range or out-of range variables."""


class ArgumentException(ToolkitException):
    """Exception raised for invalid arguments/missing inputs."""


class DocumentationException(ToolkitException):
    """Exception raised for invalid/missing documentation."""


class TestingException(ToolkitException):
    """Exception raised for invalid/missing/failing tests."""

class RuntimeException(ToolkitException):
    """Exception raised for general runtime errors."""


def ex_assert(condition: bool, exception: Exception):
    """Raise an exception if a condition is not met

    Args:
        condition (bool): Condition to be met
        exception (Exception): Exception to be raised

    Raises:
        exception: If condition is not met
    """
    if not condition:
        raise exception

_EPSILON = 10**-7

_UNICODE_DIGITS = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "-": "⁻"
}

def parse_interval(interval_string: str) -> tuple[float, float]:
    """
    Expects input of the form:
    (a, b) (a, b] [a, b) [a, b]
    Parses it into a list of 2 elements which are an inclusive range.

    Args:
        interval_string (str): String to be parsed

    Returns:
        tuple[float, float]: Tuple containing upper and lower bounds of the interval (inclusive)
    """
    components = interval_string.strip().split(",")

    ex_assert(len(components) == 2, ArgumentException("Invalid interval string"))

    interval: tuple[float, float] = (
        float(components[0][1:]) + (_EPSILON if components[0][0] == "(" else 0),
        float(components[1][:-1]) - (_EPSILON if components[1][-1] == ")" else 0),
    )

    return interval

def stringify_interval(interval: tuple[float, float]) -> str:
    """
    Turns a physical range back into its string representation.
    Args:
        interval (tuple[float, float]): interval in tuple form

    Returns:
        str: interval in string form
    """
    # We try to undo the epsilon for clarity, but this will not work if the original input was non-integral
    if interval[0] == float('inf'):
        bottom_range = "(inf, "
    else:
        bottom_range = f"({int(interval[0])}, " if (interval[0] - _EPSILON).is_integer() else f"[{interval[0]}, "

    if interval[1] == float('inf'):
        top_range = "inf)"
    else:
        top_range = f"{int(interval[1] - _EPSILON)})" if (interval[1] + _EPSILON).is_integer() else f"{interval[1]}]"

    return bottom_range + top_range

def _safe_div(dividend: float, divisor: float) -> float:
    """
    Float division, with infinity returned if dividing by 0
    Args:
        dividend (float): float being divided
        divisor (float): float dividing

    Returns:
        float: Result of regular division, or infinity if the divisor is 0
    """
    if divisor == 0:
        return copysign(float("inf"), dividend)
    return dividend / divisor

def _safe_min(args: Iterable[float]) -> float:
    """
    Calculate the minimum of an iterable, without returning nan
    Args:
        args (Iterable[float]): iterable for which to find a minimum

    Returns:
        float: minimum of args, ignoring nan
    """
    filtered_args = (arg for arg in args if not isnan(arg))
    return min(filtered_args)

def _safe_max(args: Iterable[float]) -> float:
    """
    Calculate the maximum of an iterable, without returning nan
    Args:
        args (Iterable[float]): iterable for which to find a maximum

    Returns:
        float: maximum of args, ignoring nan
    """
    filtered_args = (arg for arg in args if not isnan(arg))
    return max(filtered_args)

def physical_range_division(prange_a: tuple[float, float], prange_b: tuple[float, float]) -> tuple[float, float]:
    """
    Calculate the maximum physical range possible from the equation:
        a / b
    Args:
        prange_a (tuple[float, float]): physical range of 'a'
        prange_b (tuple[float, float]): physical range of 'b'

    Returns:
        tuple[float, float]: physical range of 'a / b'
    """
    range_combinations = (_safe_div(prange_a[0], prange_b[0]), _safe_div(prange_a[0], prange_b[1]),
                          _safe_div(prange_a[1], prange_b[0]), _safe_div(prange_a[1], prange_b[1]))
    if prange_b[0] <= 0 <= prange_b[1]:
        range_combinations = (*range_combinations,
                               copysign(float("inf"), prange_a[0]), copysign(float("inf"), prange_a[1]))
    return (_safe_min(range_combinations), _safe_max(range_combinations))

def physical_range_multiplication(prange_a: tuple[float, float], prange_b: tuple[float, float]) -> tuple[float, float]:
    """
    Calculate the maximum physical range possible from the equation:
        a * b
    Args:
        prange_a (tuple[float, float]): physical range of 'a'
        prange_b (tuple[float, float]): physical range of 'b'

    Returns:
        tuple[float, float]: physical range of 'a * b'
    """
    range_combinations = (prange_a[0] * prange_b[0], prange_a[0] * prange_b[1],
                          prange_a[1] * prange_b[0], prange_a[1] * prange_b[1])
    return (_safe_min(range_combinations), _safe_max(range_combinations))

def physical_range_power(prange: tuple[float, float], power: int) -> tuple[float, float]:
    """
    Calculate the maximum physical range possible from the equation:
        a ** n
    Args:
        prange (tuple[float, float]): physical range of 'a'
        power (int): exponentiating power

    Returns:
        tuple[float, float]: physical range of 'a ** n'
    """
    if power % 2 == 0:
        if prange[0] <= 0 and prange[1] <= 0:
            return (prange[1] ** power, prange[0] ** power)

        if prange[0] <= 0 <= prange[1]:
            return (prange[0] * prange[1] ** power if prange[0] < 0 else 0,
                    prange[1] ** power)
    else:
        if prange[0] <= 0 and prange[1] <= 0:
            return (prange[0] ** power, prange[1] ** power)

        if prange[0] <= 0 <= prange[1]:
            max_power = max(abs(prange[0]), prange[1]) ** (power - 1)
            return (prange[0] * max_power if prange[0] < 0 else 0,
                    prange[1] * max_power)

    # prange[0] >= 0 here
    return (prange[0] ** power, prange[1] ** power)

def exponent_unicode(exponent: int) -> str:
    """
    Get the unicode superscript of an integer
    Args:
        exponent (int): integer exponent

    Returns:
        str: exponent unicode
    """
    return "".join(_UNICODE_DIGITS[digit] for digit in str(exponent))

def map_dictionary_value(
    function: Callable[[U], V], dictionary: dict[T, U]
) -> dict[T, V]:
    """Map a function over the values of a dictionary

    Args:
        function (Callable[[U], V]): Mapping function
        dictionary (dict[T, U]): Dictionary to be mapped over

    Returns:
        dict[T, V]: Mapped dictionary
    """
    return dict(map(lambda t: (t[0], function(t[1])), dictionary.items()))


def map_dictionary_key(
    function: Callable[[T], V], dictionary: dict[T, U]
) -> dict[V, U]:
    """Map a function over the keys of a dictionary

    Args:
        function (Callable[[T], V]): Mapping function
        dictionary (dict[T, U]): Dictionary to be mapped over

    Returns:
        dict[V, U]: Mapped dictionary
    """
    return dict(map(lambda t: (function(t[0]), t[1]), dictionary.items()))
