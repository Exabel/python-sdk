import sys
import warnings
from contextlib import contextmanager
from typing import Iterator, Mapping

_OPTIONAL_DEPENDENCIES = {
    "snowflake": "snowflake-connector-python",
    "snowflake.sqlalchemy": "snowflake-sqlalchemy",
    "sqlalchemy": "sqlalchemy",
    "openpyxl": "openpyxl",
}


@contextmanager
def handle_missing_imports(module_library_map: Mapping[str, str] = None) -> Iterator:
    """
    Handle import errors when importing modules that can be missing. `module_library_map` is a
    mapping from module name to library name on PyPI.
    """
    module_library_map = module_library_map or _OPTIONAL_DEPENDENCIES
    try:
        yield
    except ImportError as e:
        if e.name in module_library_map:
            # Get the caller's module name. Second frame is `contextlib` because of the decorator.
            # Third frame is the caller of this function.
            caller_name = sys._getframe(2).f_locals.get(  # pylint: disable=protected-access
                "__name__"
            )
            warnings.warn(
                f"Module '{e.name}' not found. The library '{module_library_map[str(e.name)]}' "
                "does not seem to be installed. Please install this library to use the "
                f"'{caller_name}' module.",
            )
            return
        raise
