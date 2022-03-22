from exabel_data_sdk.client.api.api_client.derived_signal_api_client import DerivedSignalApiClient
from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    CreateDerivedSignalRequest,
    DeleteDerivedSignalRequest,
    DerivedSignal,
    GetDerivedSignalRequest,
    UpdateDerivedSignalRequest,
)


class DerivedSignalHttpClient(DerivedSignalApiClient, BaseHttpClient):
    """
    Client which sends derived signal requests to the Exabel Analytics API with JSON over HTTP.
    """

    def create_derived_signal(self, request: CreateDerivedSignalRequest) -> DerivedSignal:
        return self._request("POST", "derivedSignals", DerivedSignal(), body=request.signal)

    def get_derived_signal(self, request: GetDerivedSignalRequest) -> DerivedSignal:
        return self._request("GET", request.name, DerivedSignal())

    def update_derived_signal(self, request: UpdateDerivedSignalRequest) -> DerivedSignal:
        return self._request("PATCH", "derivedSignals", DerivedSignal(), body=request.signal)

    def delete_derived_signal(self, request: DeleteDerivedSignalRequest) -> None:
        return self._request("DELETE", f"{request.name}", None)
