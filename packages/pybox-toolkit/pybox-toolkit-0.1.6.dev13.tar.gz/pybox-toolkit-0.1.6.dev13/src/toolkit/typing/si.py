""" Definitions for all the SI units """

from toolkit.typing import Unit

class Second(Unit):
    """ SI unit for time """
    units = "s"
    physical_range = "(-inf, inf)"

class Meter(Unit):
    """ SI unit for length """
    units = "m"
    physical_range = "[0, inf)"

class Kilogram(Unit):
    """ SI unit for weight """
    units = "kg"
    physical_range = "[0, inf)"

class Ampere(Unit):
    """ SI unit for electrical current """
    units = "A"
    physical_range = "(-inf, inf)"

class Kelvin(Unit):
    """ SI unit for thermodynamic temperature """
    units = "K"
    physical_range = "[0, inf)"

class Mole(Unit):
    """ SI unit for amounts of substance """
    units = "mol"
    physical_range = "[0, inf)"

class Candela(Unit):
    """ SI unit for luminous intensity """
    units = "cd"
    physical_range = "[0, inf)"
