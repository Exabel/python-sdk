"""This file aliases an import for backwards compatibility after an exception object was renamed."""
# pylint: disable=unused-import
from exabel_data_sdk.services.file_loading_exception import (
    FileLoadingException as CsvLoadingException,
)
