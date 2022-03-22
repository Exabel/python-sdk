from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.api.api_client.signal_api_client import SignalApiClient
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateSignalRequest,
    DeleteSignalRequest,
    GetSignalRequest,
    ListSignalsRequest,
    ListSignalsResponse,
    Signal,
    UpdateSignalRequest,
)


class SignalHttpClient(SignalApiClient, BaseHttpClient):
    """
    Client which sends signal requests to the Exabel Data API with JSON over HTTP.
    """

    def list_signals(self, request: ListSignalsRequest) -> ListSignalsResponse:
        return self._request("GET", "signals", ListSignalsResponse(), body=request)

    def get_signal(self, request: GetSignalRequest) -> Signal:
        return self._request("GET", request.name, Signal())

    def create_signal(self, request: CreateSignalRequest) -> Signal:
        return self._request(
            "POST",
            f"signals?createLibrarySignal={request.create_library_signal}",
            Signal(),
            request.signal,
        )

    def update_signal(self, request: UpdateSignalRequest) -> Signal:
        return self._request(
            "PATCH",
            request.signal.name,
            Signal(),
            request.signal,
        )

    def delete_signal(self, request: DeleteSignalRequest) -> None:
        self._request("DELETE", request.name, None)
