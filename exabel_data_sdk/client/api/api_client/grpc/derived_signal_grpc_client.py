from exabel_data_sdk.client.api.api_client.derived_signal_api_client import DerivedSignalApiClient
from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    CreateDerivedSignalRequest,
    DeleteDerivedSignalRequest,
    DerivedSignal,
    GetDerivedSignalRequest,
    UpdateDerivedSignalRequest,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2_grpc import DerivedSignalServiceStub


class DerivedSignalGrpcClient(DerivedSignalApiClient, BaseGrpcClient):
    """
    Client which sends derived signal requests to the Exabel Analytics API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.ANALYTICS_API)
        self.stub = DerivedSignalServiceStub(self.channel)

    @handle_grpc_error
    def create_derived_signal(self, request: CreateDerivedSignalRequest) -> DerivedSignal:
        return self.stub.CreateDerivedSignal(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def get_derived_signal(self, request: GetDerivedSignalRequest) -> DerivedSignal:
        return self.stub.GetDerivedSignal(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def update_derived_signal(self, request: UpdateDerivedSignalRequest) -> DerivedSignal:
        return self.stub.UpdateDerivedSignal(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def delete_derived_signal(self, request: DeleteDerivedSignalRequest) -> None:
        return self.stub.DeleteDerivedSignal(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
