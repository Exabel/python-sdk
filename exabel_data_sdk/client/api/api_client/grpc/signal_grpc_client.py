from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.api_client.signal_api_client import SignalApiClient
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateSignalRequest,
    DeleteSignalRequest,
    GetSignalRequest,
    ListSignalsRequest,
    ListSignalsResponse,
    Signal,
    UpdateSignalRequest,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2_grpc import SignalServiceStub


class SignalGrpcClient(SignalApiClient, BaseGrpcClient):
    """
    Client which sends signal requests to the Exabel Data API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        self.stub = SignalServiceStub(self.channel)

    @handle_grpc_error
    def list_signals(self, request: ListSignalsRequest) -> ListSignalsResponse:
        return self.stub.ListSignals(
            request,
            metadata=self.metadata,
            timeout=self.config.timeout,
        )

    @handle_grpc_error
    def get_signal(self, request: GetSignalRequest) -> Signal:
        return self.stub.GetSignal(
            request,
            metadata=self.metadata,
            timeout=self.config.timeout,
        )

    @handle_grpc_error
    def create_signal(self, request: CreateSignalRequest) -> Signal:
        return self.stub.CreateSignal(
            request,
            metadata=self.metadata,
            timeout=self.config.timeout,
        )

    @handle_grpc_error
    def update_signal(self, request: UpdateSignalRequest) -> Signal:
        return self.stub.UpdateSignal(
            request,
            metadata=self.metadata,
            timeout=self.config.timeout,
        )

    @handle_grpc_error
    def delete_signal(self, request: DeleteSignalRequest) -> None:
        self.stub.DeleteSignal(
            request,
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
