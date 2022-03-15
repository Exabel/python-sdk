from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.api.api_client.model_api_client import ModelApiClient
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import CreateModelRunRequest, ModelRun


class ModelHttpClient(ModelApiClient, BaseHttpClient):
    """
    Client which sends model requests to the Exabel Analytics API with JSON over gRPC.
    """

    def create_model_run(self, request: CreateModelRunRequest) -> ModelRun:
        return self._request("POST", f"{request.parent}/runs", ModelRun(), body=request.run)
