import importlib.util
from typing import Callable, TypeVar

import pytest

T = TypeVar("T")


def requires_modules(*modules: str) -> Callable[[type[T]], type[T]]:
    """
    Decorator for test classes requiring optional dependencies.

    If any module is not importable, all tests in the class are skipped.
    Works with both plain classes and unittest.TestCase subclasses.

    Args:
        *modules: Module names that must be importable (e.g., "openpyxl", "pandas")

    Example:
        @requires_modules("openpyxl", "pandas")
        class TestExcelFeatures:
            def test_read_excel(self): ...

        # If openpyxl or pandas are missing, all tests in this class are skipped.
    """
    not_importable = [m for m in modules if not _is_importable(m)]
    reason = (
        f"Module(s): '{', '.join(not_importable)}' must be available to run these tests."
        if not_importable
        else ""
    )
    skip_marker = pytest.mark.skipif(
        bool(not_importable),
        reason=reason,
    )

    def decorator(cls: type[T]) -> type[T]:
        return skip_marker(cls)

    return decorator


def _is_importable(module: str) -> bool:
    """
    Return True if a module or sub-module is importable.

    Args:
        module: Module name, can be nested (e.g., "google.cloud.bigquery")
    """
    parent_name = module.rpartition(".")[0]
    if parent_name and not importlib.util.find_spec(parent_name):
        return False
    return importlib.util.find_spec(module) is not None
