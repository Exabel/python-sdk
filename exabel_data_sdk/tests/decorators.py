import importlib.util
import unittest
from typing import Callable, Type, TypeVar

T = TypeVar("T")


def requires_modules(*modules: str) -> Callable[..., Type[T]]:
    """
    Decorator for a class containing tests that require optional dependencies.

    If the modules are not importable, the tests are skipped.
    """

    def wrapper(original_class: Type[T]) -> Type[T]:
        not_importable = []
        for module in modules:
            if not _is_importable(module):
                not_importable.append(module)
        return unittest.skipUnless(
            not not_importable,
            f"Module(s): '{', '.join(not_importable)}' must be available to run these tests.",
        )(original_class)

    return wrapper


def _is_importable(module: str) -> bool:
    """
    Checks whether a module or sub-module is importable.
    """
    parent_name = module.rpartition(".")[0]
    if parent_name and not importlib.util.find_spec(parent_name):
        return False
    return importlib.util.find_spec(module) is not None
