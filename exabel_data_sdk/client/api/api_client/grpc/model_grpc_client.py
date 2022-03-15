from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.api_client.model_api_client import ModelApiClient
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import CreateModelRunRequest, ModelRun
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2_grpc import ModelServiceStub


class ModelGrpcClient(ModelApiClient, BaseGrpcClient):
    """
    Client which sends model requests to the Exabel Analytics API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        self.stub = ModelServiceStub(self.channel)

    @handle_grpc_error
    def create_model_run(self, request: CreateModelRunRequest) -> ModelRun:
        return self.stub.CreateModelRun(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
