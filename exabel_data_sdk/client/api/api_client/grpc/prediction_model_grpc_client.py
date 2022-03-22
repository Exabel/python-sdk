from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.api_client.prediction_model_api_client import (
    PredictionModelApiClient,
)
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    CreatePredictionModelRunRequest,
    PredictionModelRun,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2_grpc import PredictionModelServiceStub


class PredictionModelGrpcClient(PredictionModelApiClient, BaseGrpcClient):
    """
    Client which sends prediction model requests to the Exabel Analytics API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        self.stub = PredictionModelServiceStub(self.channel)

    @handle_grpc_error
    def create_model_run(self, request: CreatePredictionModelRunRequest) -> PredictionModelRun:
        return self.stub.CreatePredictionModelRun(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
