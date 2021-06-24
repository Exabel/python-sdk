from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.api_client.time_series_api_client import TimeSeriesApiClient
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    BatchDeleteTimeSeriesPointsRequest,
    CreateTimeSeriesRequest,
    DeleteTimeSeriesRequest,
    GetTimeSeriesRequest,
    ListTimeSeriesRequest,
    ListTimeSeriesResponse,
    TimeSeries,
    UpdateTimeSeriesRequest,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2_grpc import TimeSeriesServiceStub


class TimeSeriesGrpcClient(TimeSeriesApiClient, BaseGrpcClient):
    """
    Client which sends time series requests to the Exabel Data API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        self.stub = TimeSeriesServiceStub(self.channel)

    @handle_grpc_error
    def list_time_series(self, request: ListTimeSeriesRequest) -> ListTimeSeriesResponse:
        return self.stub.ListTimeSeries(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def get_time_series(self, request: GetTimeSeriesRequest) -> TimeSeries:
        return self.stub.GetTimeSeries(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def create_time_series(self, request: CreateTimeSeriesRequest) -> TimeSeries:
        return self.stub.CreateTimeSeries(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def update_time_series(self, request: UpdateTimeSeriesRequest) -> TimeSeries:
        return self.stub.UpdateTimeSeries(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def delete_time_series(self, request: DeleteTimeSeriesRequest) -> None:
        self.stub.DeleteTimeSeries(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def batch_delete_time_series_points(self, request: BatchDeleteTimeSeriesPointsRequest) -> None:
        self.stub.BatchDeleteTimeSeriesPoints(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
