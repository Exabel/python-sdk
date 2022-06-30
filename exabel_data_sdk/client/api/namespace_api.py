from typing import Sequence

from exabel_data_sdk.client.api.api_client.grpc.namespace_grpc_client import NamespaceGrpcClient
from exabel_data_sdk.client.api.api_client.http.namespace_http_client import NamespaceHttpClient
from exabel_data_sdk.client.api.data_classes.namespace import Namespace
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import ListNamespacesRequest


class NamespaceApi:
    """
    API class for retrieving namespace info from the Data API.
    """

    def __init__(self, config: ClientConfig, use_json: bool = False):
        self.client = NamespaceHttpClient(config) if use_json else NamespaceGrpcClient(config)

    def list_namespaces(self) -> Sequence[Namespace]:
        """Lists the namespaces available to the client."""
        response = self.client.list_namespaces(ListNamespacesRequest())
        return [Namespace.from_proto(n) for n in response.namespaces]
