from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.api.api_client.prediction_model_api_client import (
    PredictionModelApiClient,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    CreatePredictionModelRunRequest,
    PredictionModelRun,
)


class PredictionModelHttpClient(PredictionModelApiClient, BaseHttpClient):
    """
    Client which sends prediction model requests to the Exabel Analytics API with JSON over HTTP.
    """

    def create_model_run(self, request: CreatePredictionModelRunRequest) -> PredictionModelRun:
        return self._request(
            "POST", f"{request.parent}/runs", PredictionModelRun(), body=request.run
        )
