from exabel_data_sdk.client.api.api_client.data_set_api_client import DataSetApiClient
from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateDataSetRequest,
    DataSet,
    DeleteDataSetRequest,
    GetDataSetRequest,
    ListDataSetsRequest,
    ListDataSetsResponse,
    UpdateDataSetRequest,
)


class DataSetHttpClient(DataSetApiClient, BaseHttpClient):
    """
    Client which sends data set requests to the Exabel Data API with JSON over HTTP.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.DATA_API)

    def list_data_sets(self, request: ListDataSetsRequest) -> ListDataSetsResponse:
        return self._request("GET", "dataSets", ListDataSetsResponse())

    def get_data_set(self, request: GetDataSetRequest) -> DataSet:
        return self._request("GET", request.name, DataSet())

    def create_data_set(self, request: CreateDataSetRequest) -> DataSet:
        return self._request("POST", "dataSets", DataSet(), body=request.data_set)

    def update_data_set(self, request: UpdateDataSetRequest) -> DataSet:
        return self._request("PATCH", "dataSets", DataSet(), body=request.data_set)

    def delete_data_set(self, request: DeleteDataSetRequest) -> None:
        return self._request("DELETE", request.name, None)
