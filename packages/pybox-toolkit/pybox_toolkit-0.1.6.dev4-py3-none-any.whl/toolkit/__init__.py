"""Toolkit is a library for creating and testing formulas."""

import sys
from collections import defaultdict
from typing import Any, Callable, Optional, Union
from sys import stdout

import sympy
from sympy.core.basic import Basic as SympyBasic
from typing_extensions import Type, TypeVar, Self


from toolkit import test
from toolkit.typing import Unit, _UnitClassParser
from toolkit.utils import (
    parse_interval,
    ArgumentException,
    DocumentationException,
    RangeException,
    RuntimeException,
    TestingException,
    ex_assert,
)

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")

class BaseFormula:
    """
    Contains information about a formula, including:
            - Parameter ranges
            - Labels
            - Documentation
    """

    formulas: list[Self] = []
    outputs: list[tuple[str, Unit]] = []
    tentative_ranges: dict[str, str] = {}
    test_class: test.ToolkitTests = None

    def __init__(self, function: Callable[..., Any], **kwargs):
        if "outputs" not in kwargs:
            raise ArgumentException(
                f"Function '{function.__qualname__}' does not have any outputs defined"
            )

        if function.__doc__ is None:
            raise DocumentationException(
                f'''Function '{function.__qualname__}' is not properly documented, please add a docstring:
	def myfunction(a: Unit):
		...

	def myfunction(a: Unit):
		""" My docstring """
	'''
            )

        self.__dict__.update(kwargs)
        self.docs: str = function.__doc__
        self.function: Callable[..., Any] = function
        self.num_args: int = function.__code__.co_argcount
        self.arg_names: list[str] = function.__code__.co_varnames[:self.num_args]
        self.name: str = function.__qualname__.replace("_", " ").title()
        self.parsed_ranges: defaultdict[str, tuple[float, float]] = defaultdict(dict)
        self.variable_types: dict[str, Unit] = {}

        for variable in self.arg_names:
            if variable not in function.__annotations__:
                raise ArgumentException(
                    f"Variable '{variable}' in '{function.__qualname__}' is missing a type"
                )

            self.variable_types[variable] = function.__annotations__[variable]
            self.parse_variable(variable, self.variable_types[variable])

        for output_name, output_type in self.outputs:
            self.variable_types[output_name] = output_type
            self.parse_variable(output_name, output_type)

        if "tentative_ranges" in self.__dict__:
            for variable, tentative_range in self.tentative_ranges.items():
                self.parsed_ranges[variable]["tentative"] = parse_interval(
                    tentative_range
                )

        BaseFormula.formulas.append(self)

    def filter_variable_dictionary(
        self, variable_dic: dict[str, Union[float, int]]
    ) -> bool:
        """Filter a dictionary of variables to see if they are in the physical range

        Args:
            variable_dic (dict[str, Union[float, int]]): Dictionary of variables to be checked

        Returns:
            bool: True if all variables are in the physical range, False otherwise
        """
        for name, value in variable_dic.items():
            if not self.in_physical_range(name, value):
                return False
        return True

    def in_physical_range(self, name: str, value: Union[float, int]) -> bool:
        """Check if a value is in the physical range of a variable

        Args:
            name (str): Dictionary key of the variable
            value (Union[float, int]): Value to be checked

        Raises:
            RangeException: If the variable range was not parsed.

        Returns:
            bool: True if the value is in the physical range, False otherwise.
        """
        if name not in self.parsed_ranges:
            raise RangeException(
                f"Could not check the physical range of '{name}', it was not parsed"
            )

        physical_range = self.parsed_ranges[name]["physical"]

        return physical_range[0] <= value <= physical_range[1]

    def parse_variable(self, variable: str, variable_type_instance: Unit):
        """Parse a variable and add it to the parsed_ranges dictionary

        Args:
            variable (str): Name of the variable
            variable_class (Unit): Unit class of the variable

        Raises:
            ArgumentException: If the variable class is not derived from Unit
        """
        if not isinstance(variable_type_instance, Unit):
            if isinstance(variable_type_instance, _UnitClassParser):
                raise ArgumentException(
                    f"Variable '{variable}' does not have an argument description"
                )

            raise ArgumentException(
                f"Variable '{variable}' has a class not derived from Unit"
            )

        self.parsed_ranges[variable]["physical"] = variable_type_instance.parsed_physical_range

    def run_tests(self, output_stream = stdout) -> bool:
        """Run all tests for this formula

        Raises:
            TestingException: If the formula does not have a test class

        Returns:
            bool: True if all tests passed, False otherwise
        """

        if "test_class" not in self.__dict__:
            raise TestingException(
                f"Cannot run tests for: '{self.function.__qualname__}', a test class was not provided."
            )
        return test.run_testcase(self.test_class, output_stream).wasSuccessful()


def __formula(
    function_class: Type[BaseFormula],
    function: Optional[Callable[..., Any]],
    **kwargs,
) -> BaseFormula:
    """The expression used in a decorator is evaluated before use, so passing in variables to the wrapper
    will actually evaluate the wrapper before passing in the function.
    We can use currying to bypass this by returning a new wrapper that actually gets the function as an argument.

    Args:
        function_class (Type[BaseFormula]): Formula class (type).
        function (Optional[Callable[..., Any]]): Function to be wrapped.

    Returns:
        BaseFormula: Wrapped formula object.
    """
    if function:
        return function_class(function)

    def wrapper(function: Optional[Callable[..., Any]]) -> BaseFormula:
        return function_class(function, **kwargs)

    return wrapper


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


class _PureFormula(BaseFormula):
    def __init__(self, function: Callable[..., SympyBasic], **kwargs):
        super().__init__(function, **kwargs)
        self.variable_symbols: dict[str, sympy.Symbol] = {}

        for variable in self.variable_types:
            self.variable_symbols[variable] = sympy.Symbol(variable)

        sympy_function_inputs = [
            self.variable_symbols[i] for i in self.arg_names
        ]
        sympy_function = function(*sympy_function_inputs)
        if not isinstance(sympy_function, tuple):
            sympy_function = (sympy_function,)

        self.sympy_equations = tuple(
            sympy.Eq(equation, self.variable_symbols[output[0]])
            for (equation, output) in zip(sympy_function, self.outputs)
        )
        self.cached_lambdas = {}

    def execute_lambda_dictionary_list(
        self,
        dic_list: list[dict[str, SympyBasic]],
        kwargs: dict[str, int],
        argument_list: list[str],
    ) -> list[dict[str, Union[float, int]]]:
        """Execute a list of dictionaries of lambdified functions over provided arguments.
        We support multiple outputs per function, so each dictionary contains the funcion for a single output.
        The lambda dictionary contains one lambda per output variable.

        Note: order of the arguments must be preserved as we're using them to cache the lambdified functions.

        Args:
            dic_list (list[dict[str, SympyBasic]]): List of dictionaries containing lambdified functions
            kwargs (dict[str, int]): Dictionary of argument values to be passed into the lambdified functions
            argument_list (list[str]): List of arguments to be passed into the lambdified functions

        Raises:
            RuntimeException: If no outputs were produced

        Returns:
            list[dict[str, Union[float, int]]]: List of dictionaries containing the outputs of the lambdified functions
        """
        # Please do not write code like this, thank you and bye
        results = list(
            map(
                lambda dic: map_dictionary_value(
                    lambda lambdified: float(lambdified(
                        *(kwargs[arg] for arg in argument_list)
                    )),
                    dic,
                ),
                dic_list,
            )
        )

        # Add a filter to check that the outputs are physically possible
        results = list(filter(self.filter_variable_dictionary, results))

        if len(results) == 0:
            raise RuntimeException(
                f"No outputs were produced for '{self.name}' with arguments {argument_list}. It may have been insufficient to solve the equation"  # pylint: disable=line-too-long
            )

        return results

    def __call__(
        self, *args: tuple[Unit, ...], **kwargs
    ) -> list[dict[str, float]]:
        """Execute the formula with the provided arguments

        Raises:
            RangeException: If any of the arguments are outside of their physical range

        Returns:
            list[dict[str, float]]: List of dictionaries containing outputs of the formula
                                          (one dictionary per possible solution)
        """
        if len(args) == self.num_args or set(kwargs) == set(self.arg_names):
            inputs = args if len(args) == self.num_args else [kwargs[i] for i in self.arg_names]
            for name, value in zip(self.arg_names, inputs):
                if not self.in_physical_range(name, value):
                    raise RangeException(
                        f"Variable '{name}' outside of physical range: {self.parsed_ranges[name]['physical']}"
                    )

            result = self.function(*args, **kwargs)
            if not isinstance(result, tuple):
                result = (result,)
            return [dict(zip(map(lambda x: x[0], self.outputs), result))]

        for name, value in kwargs.items():
            if not self.in_physical_range(name, value):
                raise RangeException(
                    f"Variable '{name}' outside of physical range: {self.parsed_ranges[name]['physical']}"
                )

        argument_list = tuple(sorted((i for i in kwargs)))
        non_argument_list = sorted((i for i in self.variable_types if i not in kwargs))
        if argument_list in self.cached_lambdas:
            return self.execute_lambda_dictionary_list(
                self.cached_lambdas[argument_list], kwargs, argument_list
            )

        known_symbols = [self.variable_symbols[arg] for arg in argument_list]
        unknown_symbols = [self.variable_symbols[sym] for sym in non_argument_list]

        # This shit either returns a dictionary of independent variables
        # or a list of tuples of dependent equations
        solved = sympy.solve(self.sympy_equations, *unknown_symbols)

        # If we get a list of tuples, we turn it into a list of dictionaries where the keys are the output names
        # Otherwise we wrap in a list for easy
        if isinstance(solved, list):
            solved = [
                dict(zip(non_argument_list, equation_tuple))
                for equation_tuple in solved
            ]
        else:
            # Solve will return a dictionary with symbol keys, we would really appreciate strings for the
            # in physical range checks
            solved = [map_dictionary_key(str, solved)]

        # We map over the dictionaries entries to get the lambdas tied to each variable
        lambdifieds = list(
            map(
                lambda dic: map_dictionary_value(
                    lambda equation: sympy.lambdify(known_symbols, equation),
                    dic,
                ),
                solved,
            )
        )

        self.cached_lambdas[argument_list] = lambdifieds

        return self.execute_lambda_dictionary_list(lambdifieds, kwargs, argument_list)


class _ImpureFormula(BaseFormula):
    def __call__(self, *args: tuple[Unit, ...], **kwargs) -> list[dict[str, float, int]]:
        """Call the impure formula.

        Raises:
            RangeException: If any of the arguments are outside of their physical range.

        Returns:
            Any: output arguments.
        """
        function_arguments = self.arg_names
        if len(args) == self.num_args:
            inputs = args
        else:
            if set(kwargs) != set(function_arguments):
                raise ArgumentException(f"""Keyword arguments for impure expression must match its arguments:
                {tuple(kwargs)} does not match {function_arguments} for {self.name}.""")
            inputs = [kwargs[i] for i in self.arg_names]

        for name, value in zip(self.arg_names, inputs):
            if not self.in_physical_range(name, value):
                raise RangeException(
                    f"Variable '{name}' outside of physical range: {self.parsed_ranges[name]['physical']}"
                )

        result = self.function(*args, **kwargs)
        if not isinstance(result, tuple):
            result = (result,)
        return [dict(zip(map(lambda x: x[0], self.outputs), result))]

def PureFormula(  # pylint: disable=invalid-name
    func: Optional[Callable[..., SympyBasic]] = None, **kwargs
) -> _PureFormula:
    """Annotation for the pure formulas.
    These formulas can only contain sympy functions and operations, and must return a single sympy expression.

    The advantage of using this annotation is that the formula will support expressing
    any varaiable out of the expression, making the formula much nicer to use.

    Args:
        func (Callable[..., SympyBasic], optional): The implementation of the pure function. Defaults to None.

    Returns:
        __PureFormula: The formula object.
    """
    return __formula(_PureFormula, func, **kwargs)


def ImpureFormula(  # pylint: disable=invalid-name
    func: Optional[Callable[..., Union[Unit, tuple[Unit, ...]]]] = None, **kwargs
) -> _ImpureFormula:
    """Annotation for the impure formulas. These formulas can contain any python code.


    Args:
        func (Optional[Callable[..., Union[Unit, tuple[Unit, ...]]]], optional): Function implementation. Default: None.

    Returns:
        __ImpureFormula: The formula object.
    """
    return __formula(_ImpureFormula, func, **kwargs)
