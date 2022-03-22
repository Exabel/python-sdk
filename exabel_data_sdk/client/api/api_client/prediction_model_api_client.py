from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    CreatePredictionModelRunRequest,
    PredictionModelRun,
)


class PredictionModelApiClient(ABC):
    """
    Superclass for clients that sends prediction model requests to the Exabel Analytics API.
    """

    @abstractmethod
    def create_model_run(self, request: CreatePredictionModelRunRequest) -> PredictionModelRun:
        """Create a prediction model run."""
