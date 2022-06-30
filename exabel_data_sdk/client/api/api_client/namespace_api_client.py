from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    ListNamespacesRequest,
    ListNamespacesResponse,
)


class NamespaceApiClient(ABC):
    """
    Superclass for clients that send namespace requests to the Exabel Data API.
    """

    @abstractmethod
    def list_namespaces(self, request: ListNamespacesRequest) -> ListNamespacesResponse:
        """Lists the namespaces available to the client."""
