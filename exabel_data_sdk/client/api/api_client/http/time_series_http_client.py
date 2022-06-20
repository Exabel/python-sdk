from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.api.api_client.time_series_api_client import TimeSeriesApiClient
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    BatchDeleteTimeSeriesPointsRequest,
    CreateTimeSeriesRequest,
    DeleteTimeSeriesRequest,
    GetTimeSeriesRequest,
    ImportTimeSeriesRequest,
    ImportTimeSeriesResponse,
    ListTimeSeriesRequest,
    ListTimeSeriesResponse,
    TimeSeries,
    UpdateTimeSeriesRequest,
)


class TimeSeriesHttpClient(TimeSeriesApiClient, BaseHttpClient):
    """
    Client which sends time series requests to the Exabel Data API with JSON over HTTP.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.DATA_API)

    def list_time_series(self, request: ListTimeSeriesRequest) -> ListTimeSeriesResponse:
        return self._request(
            "GET", f"{request.parent}/timeSeries", ListTimeSeriesResponse(), body=request
        )

    def get_time_series(self, request: GetTimeSeriesRequest) -> TimeSeries:
        return self._request("GET", request.name, TimeSeries(), body=request)

    def create_time_series(self, request: CreateTimeSeriesRequest) -> TimeSeries:
        return self._request(
            "POST",
            f"{request.time_series.name}?createTag={request.create_tag}",
            TimeSeries(),
            body=request.time_series,
        )

    def update_time_series(self, request: UpdateTimeSeriesRequest) -> TimeSeries:
        # Due to a mistake in the proto definition of UpdateTimeSeries, where an additional binding
        # is listed as a POST instead of a PATCH, this method only works if the time series resource
        # name is created with the entity before the signal (while in principle both orders should
        # work).
        name = request.time_series.name
        if name.startswith("signal"):
            parts = name.split("/")
            assert len(parts) == 6
            name = f"{parts[2]}/{parts[3]}/{parts[4]}/{parts[5]}/{parts[0]}/{parts[1]}"
        return self._request("PATCH", name, TimeSeries(), body=request.time_series)

    def import_time_series(self, request: ImportTimeSeriesRequest) -> ImportTimeSeriesResponse:
        raise NotImplementedError("Import time series is not implemented for the HTTP client.")

    def delete_time_series(self, request: DeleteTimeSeriesRequest) -> None:
        self._request("DELETE", request.name, None)

    def batch_delete_time_series_points(self, request: BatchDeleteTimeSeriesPointsRequest) -> None:
        self._request("POST", f"{request.name}/points:batchDelete", None, body=request)
