from typing import Sequence

from exabel_data_sdk.client.api.resource_creation_result import ResourceCreationResult


class FileLoadingException(Exception):
    """Represents an error that occurred during the loading of a data file."""

    def __init__(self, message: str, *, failures: Sequence[ResourceCreationResult] = None):
        super().__init__(message)
        self.message = message
        self.failures = failures
