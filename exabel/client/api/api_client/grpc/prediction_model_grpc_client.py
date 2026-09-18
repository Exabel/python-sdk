import json

from exabel.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel.client.api.api_client.grpc.base_grpc_client import (
    DEFAULT_BACKOFF_MULTIPLIER,
    DEFAULT_INITIAL_BACKOFF_SECONDS,
    DEFAULT_MAX_ATTEMPTS,
    DEFAULT_MAX_BACKOFF_SECONDS,
    BaseGrpcClient,
)
from exabel.client.api.api_client.prediction_model_api_client import (
    PredictionModelApiClient,
)
from exabel.client.api.error_handler import handle_grpc_error
from exabel.client.client_config import ClientConfig
from exabel.stubs.exabel.api.analytics.v1.all_pb2 import (
    CreatePredictionModelRequest,
    CreatePredictionModelRunRequest,
    DeletePredictionModelRequest,
    GetPredictionModelRequest,
    GetPredictionModelRunRequest,
    ListPredictionModelRunsRequest,
    ListPredictionModelRunsResponse,
    ListPredictionModelsRequest,
    ListPredictionModelsResponse,
    PredictionModel,
    PredictionModelRun,
    UpdatePredictionModelRequest,
)
from exabel.stubs.exabel.api.analytics.v1.all_pb2_grpc import PredictionModelServiceStub


class PredictionModelGrpcClient(PredictionModelApiClient, BaseGrpcClient):
    """
    Client which sends prediction model requests to the Exabel Analytics API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.ANALYTICS_API)
        self.stub = PredictionModelServiceStub(self.channel)

    def _get_service_config(
        self,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        initial_backoff: float = DEFAULT_INITIAL_BACKOFF_SECONDS,
        max_backoff: float = DEFAULT_MAX_BACKOFF_SECONDS,
        backoff_multiplier: int = DEFAULT_BACKOFF_MULTIPLIER,
    ) -> str:
        """Disable policy retries for creation, which has no idempotency key."""
        config = json.loads(
            super()._get_service_config(
                max_attempts, initial_backoff, max_backoff, backoff_multiplier
            )
        )
        config["methodConfig"].append(
            {
                "name": [
                    {
                        "service": "exabel.api.analytics.v1.PredictionModelService",
                        "method": "CreatePredictionModel",
                    },
                    {
                        "service": "exabel.api.analytics.v1.PredictionModelService",
                        "method": "CreatePredictionModelRun",
                    },
                ]
            }
        )
        return json.dumps(config)

    @handle_grpc_error
    def create_model_run(self, request: CreatePredictionModelRunRequest) -> PredictionModelRun:
        return self.stub.CreatePredictionModelRun(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def get_model(self, request: GetPredictionModelRequest) -> PredictionModel:
        """GetPredictionModel."""
        return self.stub.GetPredictionModel(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def list_models(self, request: ListPredictionModelsRequest) -> ListPredictionModelsResponse:
        """ListPredictionModels."""
        return self.stub.ListPredictionModels(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def create_model(self, request: CreatePredictionModelRequest) -> PredictionModel:
        """CreatePredictionModel."""
        return self.stub.CreatePredictionModel(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def update_model(self, request: UpdatePredictionModelRequest) -> PredictionModel:
        """UpdatePredictionModel."""
        return self.stub.UpdatePredictionModel(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def delete_model(self, request: DeletePredictionModelRequest) -> None:
        """Delete a prediction model."""
        self.stub.DeletePredictionModel(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def get_run(self, request: GetPredictionModelRunRequest) -> PredictionModelRun:
        """GetPredictionModelRun."""
        return self.stub.GetPredictionModelRun(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def list_runs(self, request: ListPredictionModelRunsRequest) -> ListPredictionModelRunsResponse:
        """ListPredictionModelRuns."""
        return self.stub.ListPredictionModelRuns(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
