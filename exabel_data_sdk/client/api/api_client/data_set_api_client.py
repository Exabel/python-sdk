from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateDataSetRequest,
    DataSet,
    DeleteDataSetRequest,
    GetDataSetRequest,
    ListDataSetsRequest,
    ListDataSetsResponse,
    UpdateDataSetRequest,
)


class DataSetApiClient(ABC):
    """
    Superclass for clients that send data set requests to the Exabel Data API.
    """

    @abstractmethod
    def list_data_sets(self, request: ListDataSetsRequest) -> ListDataSetsResponse:
        """List all data sets."""

    @abstractmethod
    def get_data_set(self, request: GetDataSetRequest) -> DataSet:
        """Get a data set."""

    @abstractmethod
    def create_data_set(self, request: CreateDataSetRequest) -> DataSet:
        """Create a data set."""

    @abstractmethod
    def update_data_set(self, request: UpdateDataSetRequest) -> DataSet:
        """Update a data set."""

    @abstractmethod
    def delete_data_set(self, request: DeleteDataSetRequest) -> None:
        """Delete a data set."""
