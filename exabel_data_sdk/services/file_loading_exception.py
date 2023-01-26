from typing import Generic, Optional, Sequence

from exabel_data_sdk.client.api.resource_creation_result import ResourceCreationResult
from exabel_data_sdk.services.file_loading_result import ResourceT


class FileLoadingException(Generic[ResourceT], Exception):
    """Represents an error that occurred during the loading of a data file."""

    def __init__(
        self,
        message: str,
        *,
        failures: Optional[Sequence[ResourceCreationResult[ResourceT]]] = None
    ):
        super().__init__(message)
        self.message = message
        self.failures: Optional[Sequence[ResourceCreationResult[ResourceT]]] = failures
