from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.api.api_client.namespace_api_client import NamespaceApiClient
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    ListNamespacesRequest,
    ListNamespacesResponse,
)


class NamespaceHttpClient(NamespaceApiClient, BaseHttpClient):
    """
    Client which sends namespace requests to the Exabel Data API with JSON over HTTP.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.DATA_API)

    def list_namespaces(self, request: ListNamespacesRequest) -> ListNamespacesResponse:
        raise NotImplementedError("List namespaces is not implemented for the HTTP client.")
