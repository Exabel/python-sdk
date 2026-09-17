from abc import ABC, abstractmethod

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


class PredictionModelApiClient(ABC):
    """
    Superclass for clients that send prediction model requests to the Exabel Analytics API.
    """

    @abstractmethod
    def create_model_run(self, request: CreatePredictionModelRunRequest) -> PredictionModelRun:
        """Create a prediction model run."""

    @abstractmethod
    def get_model(self, request: GetPredictionModelRequest) -> PredictionModel:
        """GetPredictionModel."""

    @abstractmethod
    def list_models(self, request: ListPredictionModelsRequest) -> ListPredictionModelsResponse:
        """ListPredictionModels."""

    @abstractmethod
    def create_model(self, request: CreatePredictionModelRequest) -> PredictionModel:
        """CreatePredictionModel."""

    @abstractmethod
    def update_model(self, request: UpdatePredictionModelRequest) -> PredictionModel:
        """UpdatePredictionModel."""

    @abstractmethod
    def delete_model(self, request: DeletePredictionModelRequest) -> None:
        """Delete a prediction model."""

    @abstractmethod
    def get_run(self, request: GetPredictionModelRunRequest) -> PredictionModelRun:
        """GetPredictionModelRun."""

    @abstractmethod
    def list_runs(self, request: ListPredictionModelRunsRequest) -> ListPredictionModelRunsResponse:
        """ListPredictionModelRuns."""
