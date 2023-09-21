"""Top-level package for Functions for jmespath python library."""

__author__ = """Karel Antonio Verdecia Ortiz"""
__email__ = 'kverdecia@gmail.com'
__version__ = '0.1.3'

from typing import Any

import jmespath

from . import functions


_OPTIONS = jmespath.Options(custom_functions=functions.Functions())


def search(condition: str, context: Any, context_function_data: dict | None = None) -> Any:
    if context_function_data is None:
        return jmespath.search(condition, context, options=_OPTIONS)
    options = jmespath.Options(custom_functions=functions.ContextFunctions(context_function_data))
    return jmespath.search(condition, context, options=options)


def index_to_coordinates(s, index):
    """Returns (line_number, col) of `index` in `s`."""
    if not len(s):
        return 1, 1
    sp = s[:index + 1].splitlines(keepends=True)
    return len(sp), len(sp[-1])
