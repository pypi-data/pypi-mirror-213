""" Data types and underlying mechanisms """
from dataclasses import dataclass
from typing import Union

from toolkit.utils import (
    parse_interval,
    stringify_interval,
    physical_range_power,
    physical_range_division,
    physical_range_multiplication,
    exponent_unicode,
    ArgumentException,
    RangeException
)

# Unit composition works through an eager simplication method.
def _simplify_type_lists(list_left: tuple[tuple["Unit", int], ...],
                                  list_right: tuple[tuple["Unit", int], ...]) -> tuple[tuple["Unit", int], ...]:
    """
    Performs algebraic simplification on two lists of type terminals
    Type terminals have the form: (type, exponent)
    The simplification assumes multiplication of the left list by the right list

    Args:
        list_left (tuple[tuple["Unit", int], ...]): left of multiplication
        list_right (tuple[tuple["Unit", int], ...]): right of multiplication

    Returns:
        tuple[tuple["Unit", int], ...]: simplified type list
    """
    unit_types = []
    types_id = {}

    for unit in list_left:
        unit_types.append(unit)
        types_id[unit[0]] = len(unit_types) - 1

    for unit_type, unit_power in list_right:
        if unit_type in types_id:
            unit_id = types_id[unit_type]
            ctype, cpower = unit_types[unit_id]
            unit_types[unit_id] = (ctype, cpower + unit_power)
        else:
            unit_types.append((unit_type, unit_power))

    return tuple(unit_types)

def _resolve_units_and_physical_range(type_list: tuple[tuple["Unit", int], ...]) -> tuple[str, tuple[float, float]]:
    """
    Transforms a type list into a unit string and a physical range (already parsed)

    Args:
        type_list (tuple[tuple["Unit", int], ...]): type list

    Returns:
        tuple[str, tuple[float, float]]: a tuple with a unit string and a parsed physical range
    """

    parsed_physical_range = [1, 1]
    units = ""

    type_tree = (tuple(unit for unit in type_list if unit[1] > 0), tuple(unit for unit in type_list if unit[1] < 0))

    if len(type_tree[0]) == 0:
        for unit_type, unit_power in type_tree[1]:
            units += (unit_type.units + exponent_unicode(unit_power))
            unit_physical_range = physical_range_power(unit_type.parsed_physical_range, -unit_power)
            parsed_physical_range = physical_range_division(parsed_physical_range, unit_physical_range)
    else:
        for unit_type, unit_power in type_tree[0]:
            units += (unit_type.units + (exponent_unicode(unit_power) if unit_power != 1 else ""))
            unit_physical_range = physical_range_power(unit_type.parsed_physical_range, unit_power)
            parsed_physical_range = physical_range_multiplication(parsed_physical_range, unit_physical_range)

        if len(type_tree[1]) != 0:
            units += "⁄"

            for unit_type, unit_power in type_tree[1]:
                units += (unit_type.units + (exponent_unicode(-unit_power) if -unit_power != 1 else ""))
                unit_physical_range = physical_range_power(unit_type.parsed_physical_range, -unit_power)
                parsed_physical_range = physical_range_division(parsed_physical_range, unit_physical_range)

    return (units, parsed_physical_range)

class _UnitClassParser(type):
    def __pow__(cls, power):
        if not isinstance(power, int):
            raise ArgumentException(f"Unit power must be an integer, '{type(power)}' provided.")

        if power == 0:
            raise ArgumentException("Unit exponent cannot be 0.")

        name = f"({cls.__name__}){power}"

        type_list = tuple((unit_type, unit_power * power) for unit_type, unit_power in cls.type_list)

        units, parsed_physical_range = _resolve_units_and_physical_range(type_list)

        new_dic = {
                    "type_list": type_list,
                    "parsed_physical_range": parsed_physical_range,
                    "units": units
                  }

        composite = cls.__class__.__new__(cls.__class__, name, cls.__bases__, new_dic)
        composite.physical_range = stringify_interval(parsed_physical_range)

        return composite

    def __truediv__(cls, other):
        if not isinstance(other, cls.__class__):
            raise ArgumentException(f"Unit division can only be by another unit, '{type(other)}' provided.")

        name = f"({cls.__name__}/{other.__name__})"

        type_list = _simplify_type_lists(
            cls.type_list,
            ((unit_type, -unit_power) for unit_type, unit_power in other.type_list)
        )

        units, parsed_physical_range = _resolve_units_and_physical_range(type_list)

        new_dic = {
                    "type_list": type_list,
                    "parsed_physical_range": parsed_physical_range,
                    "units": units
                  }

        composite = cls.__class__.__new__(cls.__class__, name, cls.__bases__, new_dic)
        composite.physical_range = stringify_interval(parsed_physical_range)

        return composite

    def __mul__(cls, other):
        if not isinstance(other, cls.__class__):
            raise ArgumentException(f"Unit multiplication can only be by another unit, '{type(other)}' provided.")

        name = f"({cls.__name__}*{other.__name__})"

        type_list = _simplify_type_lists(
            cls.type_list,
            other.type_list
        )

        units, parsed_physical_range = _resolve_units_and_physical_range(type_list)

        new_dic = {
                    "type_list": type_list,
                    "parsed_physical_range": parsed_physical_range,
                    "units": units
                  }

        composite = cls.__class__.__new__(cls.__class__, name, cls.__bases__, new_dic)
        composite.physical_range = stringify_interval(parsed_physical_range)

        return composite

    def __new__(mcs, name: str, bases: tuple[type, ...], dic: dict[str, str]):
        if "physical_range" in dic:
            if "parsed_physical_range" in dic:
                print(
                    f"Warning: parsed physical range for '{name}' has been overwritten."
                )
            dic["parsed_physical_range"] = parse_interval(dic["physical_range"])

        if "parsed_physical_range" not in dic:
            raise RangeException(
                f"A type class must have a physical range provided, not found for: '{name}'"
            )

        if "units" not in dic:
            raise ArgumentException(
                f"Type class must have units provided, not found for: '{name}'"
            )

        new_type = super().__new__(mcs, name, bases, dic)

        # We do not check hasattr here, because the Unit base class is guaranteed to have a type list
        if "type_list" not in new_type.__dict__:
            new_type.type_list = ((new_type, 1),)

        return new_type

class BaseUnit:
    """ Base units from which all units derive """
    def __init__(self, description: str, default: Union[str, float, int] = None):
        self.description = description
        self.default = default

@dataclass
class ChoiceEntry:
    """ A choice in a multiple-choice parameter """
    value: Union[str, float, int]
    name: str = None
    description: str = None

    def __init__(self, value, name = None, description = None):
        self.value = value
        self.name = str(value) if name is None else name
        self.description = description

class Choice(BaseUnit):
    """ Represents a multiple-choice parameter type in an impure formula """
    def __init__(self, choices: list[ChoiceEntry], description: str, default = None):
        self.choices = choices
        super().__init__(description, default)

        used_names = set()

        if not isinstance(choices, list):
            raise ArgumentException(
                f"Choices should be a list, '{type(choices)}' given."
            )

        if len(choices) < 2:
            raise ArgumentException(
                f"Choice parameter should have more than 2 available options, {len(choices)} given."
            )

        choice_type = type(self.choices[0].value)
        for choice in self.choices:
            if choice.name in used_names:
                raise ArgumentException(
                    f"Choice entries cannot have duplicate names, duplicate found for '{choice.name}'."
                )
            used_names.add(choice.name)

            if not isinstance(choice.value, choice_type):
                raise ArgumentException(
                    f"Types of choice entries should be homogenous, '{choice_type}' and '{type(choice.value)}' differ."
                )

        self.possible_values = set(choice.value for choice in self.choices)

    def possible(self, value: Union[float, str]) -> bool:
        """ Checks whether a unit is possible (in physical range) """
        return value in self.possible_values

class Unit(BaseUnit, metaclass=_UnitClassParser):
    """Base class for all units"""

    units: str = ""
    physical_range: str = "(-inf, inf)"
    parsed_tentative_range: tuple[float, float] = (float("-inf"), float("inf"))

    def __init__(self, description: str, tentative_range: str = None,
                 default: Union[str, float, int] = None, physical_range: str = None):
        super().__init__(description, default)

        self.description = description

        if tentative_range is not None:
            self.parsed_tentative_range = parse_interval(tentative_range)

        if physical_range is not None:
            self.parsed_physical_range = parse_interval(physical_range)
            self.physical_range = physical_range

    def possible(self, value: float) -> bool:
        """ Checks whether a unit is possible (in physical range) """
        return self.parsed_physical_range[0] <= value <= self.parsed_physical_range[1]
