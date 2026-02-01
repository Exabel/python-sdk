"""This file aliases an import for backwards compatibility after an exception object was renamed."""

from exabel_data_sdk.services.file_loading_exception import (  # noqa: F401
    FileLoadingException as CsvLoadingException,
)
