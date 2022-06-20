from abc import ABC, abstractmethod

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


class TimeSeriesApiClient(ABC):
    """
    Superclass for clients that send time series requests to the Exabel Data API.
    """

    @abstractmethod
    def list_time_series(self, request: ListTimeSeriesRequest) -> ListTimeSeriesResponse:
        """List all time series for an entity."""

    @abstractmethod
    def get_time_series(self, request: GetTimeSeriesRequest) -> TimeSeries:
        """Get a time series."""

    @abstractmethod
    def create_time_series(self, request: CreateTimeSeriesRequest) -> TimeSeries:
        """Create a time series."""

    @abstractmethod
    def update_time_series(self, request: UpdateTimeSeriesRequest) -> TimeSeries:
        """Update a time series."""

    @abstractmethod
    def import_time_series(self, request: ImportTimeSeriesRequest) -> ImportTimeSeriesResponse:
        """Import multiple time series."""

    @abstractmethod
    def delete_time_series(self, request: DeleteTimeSeriesRequest) -> None:
        """Delete a time series."""

    @abstractmethod
    def batch_delete_time_series_points(self, request: BatchDeleteTimeSeriesPointsRequest) -> None:
        """Delette part of a time series."""
