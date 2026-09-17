from exabel.client.api.api_client.dashboard_api_client import DashboardApiClient
from exabel.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel.client.api.error_handler import handle_grpc_error
from exabel.client.client_config import ClientConfig
from exabel.stubs.exabel.api.management.v1.all_pb2_grpc import DashboardServiceStub
from exabel.stubs.exabel.api.management.v1.dashboard_service_pb2 import (
    ListTableColumnsRequest,
    ListTableColumnsResponse,
    ListWidgetsRequest,
    ListWidgetsResponse,
)


class DashboardGrpcClient(DashboardApiClient, BaseGrpcClient):
    """
    Client which sends dashboard requests to the Exabel Management API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.MANAGEMENT_API)
        self.stub = DashboardServiceStub(self.channel)

    @handle_grpc_error
    def list_widgets(self, request: ListWidgetsRequest) -> ListWidgetsResponse:
        return self.stub.ListWidgets(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def list_table_columns(self, request: ListTableColumnsRequest) -> ListTableColumnsResponse:
        return self.stub.ListTableColumns(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
