from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import CreateModelRunRequest, ModelRun


class ModelApiClient(ABC):
    """
    Superclass for clients that sends model requests to the Exabel Analytics API.
    """

    @abstractmethod
    def create_model_run(self, request: CreateModelRunRequest) -> ModelRun:
        """Create a model run."""
