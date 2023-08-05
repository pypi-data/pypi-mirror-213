"""
This type stub file was generated by pyright.
"""

import collections.abc as abc
from typing import List, Tuple

import click

FAKE_OPT_NAME_LEN = ...

def get_callback_and_params(func) -> Tuple[abc.Callable, List[click.Option]]:
    """Returns callback function and its parameters list

    :param func: decorated function or click Command
    :return: (callback, params)
    """
    ...

def get_fake_option_name(name_len: int = ..., prefix: str = ...): ...
def raise_mixing_decorators_error(wrong_option: click.Option, callback: abc.Callable): ...
def resolve_wrappers(f):
    """Get the underlying function behind any level of function wrappers."""
    ...
