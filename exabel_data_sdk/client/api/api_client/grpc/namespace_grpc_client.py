from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.api_client.namespace_api_client import NamespaceApiClient
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    ListNamespacesRequest,
    ListNamespacesResponse,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2_grpc import NamespaceServiceStub


class NamespaceGrpcClient(NamespaceApiClient, BaseGrpcClient):
    """
    Client which sends namespace requests to the Exabel Data API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.DATA_API)
        self.stub = NamespaceServiceStub(self.channel)

    @handle_grpc_error
    def list_namespaces(self, request: ListNamespacesRequest) -> ListNamespacesResponse:
        return self.stub.ListNamespaces(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
