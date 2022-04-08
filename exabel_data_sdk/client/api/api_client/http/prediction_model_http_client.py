from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.api.api_client.prediction_model_api_client import (
    PredictionModelApiClient,
)
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    CreatePredictionModelRunRequest,
    PredictionModelRun,
)


class PredictionModelHttpClient(PredictionModelApiClient, BaseHttpClient):
    """
    Client which sends prediction model requests to the Exabel Analytics API with JSON over HTTP.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.ANALYTICS_API)

    def create_model_run(self, request: CreatePredictionModelRunRequest) -> PredictionModelRun:
        return self._request(
            "POST", f"{request.parent}/runs", PredictionModelRun(), body=request.run
        )
