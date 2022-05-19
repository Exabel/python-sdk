import sys
import unittest
from typing import Callable, Type, TypeVar

T = TypeVar("T")  # pylint: disable=invalid-name


def requires_modules(*modules: str) -> Callable[..., Type[T]]:
    """
    Decorator for a class containing tests that require optional dependencies.

    If the modules have not been imported, the tests are skipped.
    """

    def wrapper(original_class: Type[T]) -> Type[T]:
        unavailable_modules = set(set(modules)).difference(sys.modules)
        return unittest.skipUnless(
            not unavailable_modules,
            f"Module(s): '{', '.join(unavailable_modules)}' must be available to run these "
            "tests.",
        )(original_class)

    return wrapper
