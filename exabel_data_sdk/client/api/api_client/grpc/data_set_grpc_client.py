from exabel_data_sdk.client.api.api_client.data_set_api_client import DataSetApiClient
from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
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
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2_grpc import DataSetServiceStub


class DataSetGrpcClient(DataSetApiClient, BaseGrpcClient):
    """
    Client which sends data set requests to the Exabel Data API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.DATA_API)
        self.stub = DataSetServiceStub(self.channel)

    @handle_grpc_error
    def list_data_sets(self, request: ListDataSetsRequest) -> ListDataSetsResponse:
        return self.stub.ListDataSets(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def get_data_set(self, request: GetDataSetRequest) -> DataSet:
        return self.stub.GetDataSet(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def create_data_set(self, request: CreateDataSetRequest) -> DataSet:
        return self.stub.CreateDataSet(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def update_data_set(self, request: UpdateDataSetRequest) -> DataSet:
        return self.stub.UpdateDataSet(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def delete_data_set(self, request: DeleteDataSetRequest) -> None:
        return self.stub.DeleteDataSet(request, metadata=self.metadata, timeout=self.config.timeout)
