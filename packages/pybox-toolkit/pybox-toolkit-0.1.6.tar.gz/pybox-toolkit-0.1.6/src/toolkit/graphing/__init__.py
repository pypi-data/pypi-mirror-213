""" Provides functions related to graphing formulas. """

from typing import Callable


def generate_graphing_data( # pylint: disable=too-many-arguments
    function: Callable,
    input_variable: str,
    output_variable: str,
    input_range: tuple[float, float],
    defaults: dict[str, float],
    iterations: int = 1000,
) -> tuple[list[float], list[float]]:
    """Returns the points needed to plot a graph for a function.

    Args:
        function (Callable): The function to be graphed.
        input_variable (str): Variable on the x-axis.
        output_variable (str): Variable on the y-axis.
        input_range (tuple[float, float]): range for the input variable.
        defaults (dict[str, float]): default values for all variables not on the axis.
        iterations (int): number of points to be plotted, default = 1000

    Returns:
        tuple[list[float], list[float]]: Points on x-axis and y-axis.
    """
    # More validation is needed for after the MVP, currently it crashes under the following scenarios:
    # 1. The inputs and defaults are not sufficient to calculate an output
    # 2. The output variable is incorrect
    # 3. You don't use the proper inputs for an impure function
    # 4. You look at it wrong
    # It will also selectively pick one output in the case of multiple possible outputs, but that's not a big deal.
    delta = (input_range[1] - input_range[0]) / iterations

    x_axis = [input_range[0] + i * delta for i in range(iterations + 1)]

    # Note that this only works for one output variable, if there are multiple outputs that is an issue.
    y_axis = [function(**defaults, **{input_variable: x})[0][output_variable] for x in x_axis]

    return (x_axis, y_axis)
