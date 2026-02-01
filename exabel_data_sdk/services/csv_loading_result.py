"""This file aliases an import for backwards compatibility after the result object was renamed."""

from exabel_data_sdk.services.file_loading_result import (
    FileLoadingResult as CsvLoadingResult,  # noqa: F401
)
