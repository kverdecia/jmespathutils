"""Top-level package for Functions for jmespath python library."""

__author__ = """Karel Antonio Verdecia Ortiz"""
__email__ = 'kverdecia@gmail.com'
__version__ = '0.1.0'

from typing import Any

import jmespath

from . import functions


_OPTIONS = jmespath.Options(custom_functions=functions.Functions())


def search(condition: str, context: Any) -> Any:
    return jmespath.search(condition, context, options=_OPTIONS)


def index_to_coordinates(s, index):
    """Returns (line_number, col) of `index` in `s`."""
    if not len(s):
        return 1, 1
    sp = s[:index + 1].splitlines(keepends=True)
    return len(sp), len(sp[-1])
