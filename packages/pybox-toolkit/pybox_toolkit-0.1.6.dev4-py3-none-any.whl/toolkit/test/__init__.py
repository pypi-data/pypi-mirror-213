"""Testing framework for formula scripts"""

from __future__ import annotations

import unittest
from sys import stdout
from typing import TYPE_CHECKING, Callable, TextIO, Union
from unittest import TestResult

from typing_extensions import Any

from toolkit.utils import TestingException

if TYPE_CHECKING:
    from toolkit import BaseFormula


def compare_floats(first: float, second: float, epsilon: float = 0.00001) -> bool:
    """Compares two floats using an epsilon

    Args:
        first (float): first float
        second (float): second float
        epsilon (float): comparison epsilon

    Returns:
        bool: whether the floats are equal or not under epsilon
    """
    return abs(first - second) < epsilon


def compare_dics(first: dict[str, float], second: dict[str, float]) -> bool:
    """Compares two dictionaries to check if they're equal in terms of floats

    Args:
        first (dict[str, float]): first dictionary
        second (dict[str, float]): second dictionary

    Returns:
        bool: whether the entries are equal
    """
    return all((compare_floats(value, second[key])) for key, value in first.items())


def compare_result(
    result: dict[str, float] | list[dict[str, float]],
    expected: dict[str, float] | list[dict[str, float]],
) -> bool:
    """Compares a result and expected from toolkit

    Args:
        result (dict[str, float] | list[dict[str, float]]): result value
        expected (dict[str, float] | list[dict[str, float]]): expected value

    Returns:
        bool: whether the result and expected are equal
    """
    return all(compare_dics(a, b) for a, b in zip(result, expected))


def test(function: Callable[[], None]) -> Callable[[], None]:
    """Decorator to mark a function as a test

    Args:
        function (function): Function to be marked

    Returns:
        Callable[[], None]: The marked function
    """
    setattr(function, "_test", True)
    return function


class TestClassSetup(type):
    """Metaclass to setup the test class"""

    all_tests: list = []

    def __new__(mcs, name, bases, dic):
        dic["documented_tests"] = []
        dic["function"] = None

        new_test = super().__new__(mcs, name, bases, dic)

        if dic["__qualname__"] != "ToolkitTests":
            mcs.all_tests.append(new_test)

        return new_test


# Have a dummy of this production runs in the browser
class ToolkitTests(unittest.TestCase, metaclass=TestClassSetup):
    """Base class for all tests"""

    function: Callable[..., Any]
    documented_tests: list[tuple[dict[str, Any], list[dict[str, Any]]]]

    def documented_test(
        self,
        arguments: dict[str, Any] = None,
        expected: Union[dict[str, Any], list[dict[str, Any]]] = None,
    ):
        """Run a documented test

        Args:
            arguments (dict[str, Any], optional): Argument values to test with. Defaults to None.
            expected (Union[dict[str, Any], list[dict[str, Any]]], optional): Expected values. Defaults to None.

        Raises:
            TestingException: If the expected values do not match the actual values
        """
        if self.function is None:
            raise TestingException(
                f"Cannot used documented_test: '{self.__qualname__}' was not provided as a test class for any function"
            )
        if arguments is None or expected is None:
            raise TestingException(
                "Cannot used documented_test: arguments and expected must be provided"
            )

        result = self.function(**arguments)
        if not isinstance(expected, list):
            expected = [expected]
        if not compare_result(result, expected):
            raise TestingException(f"{expected} could does not match {result}")
        self.documented_tests.append((arguments, result))

    @classmethod
    def dump_documented_tests(cls):
        """Print all documented tests"""
        print(cls.documented_tests)


def set_function(function: BaseFormula) -> Callable[[ToolkitTests], ToolkitTests]:
    """Decorator to set the function to be tested

    Args:
        function (BaseFormula): Function to be tested

    Returns:
        Callable[[ToolkitTests], ToolkitTests]: Decorator
    """

    def wrapper(cls: ToolkitTests):
        cls.function = function
        function.test_class = cls
        return cls

    return wrapper


def run_testcase(testcase: type[ToolkitTests], output_stream: TextIO) -> TestResult:
    """Run all tests in a testcase

    Args:
        testcase (ToolkitTests): Testcase to be run

    Returns:
        TestResult: Result of the test
    """
    runner = unittest.TextTestRunner(output_stream)
    suite = unittest.TestSuite()

    for name, item in testcase.__dict__.items():
        if hasattr(item, "_test"):
            suite.addTest(testcase(name))

    return runner.run(suite)


def run_tests() -> bool:
    """Run all tests for the function

    Returns:
        bool: Whether all tests passed
    """
    tests_results = True
    for testcase in ToolkitTests.all_tests:
        print(f"Tests in {testcase.__qualname__}:\n")
        tests_results = run_testcase(testcase, stdout) and tests_results

    return tests_results
