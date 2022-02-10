from typing import Optional, Sequence

from google.protobuf.field_mask_pb2 import FieldMask

from exabel_data_sdk.client.api.api_client.grpc.data_set_grpc_client import DataSetGrpcClient
from exabel_data_sdk.client.api.api_client.http.data_set_http_client import DataSetHttpClient
from exabel_data_sdk.client.api.data_classes.data_set import DataSet
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.data_set_service_pb2 import (
    CreateDataSetRequest,
    DeleteDataSetRequest,
    GetDataSetRequest,
    ListDataSetsRequest,
    UpdateDataSetRequest,
)


class DataSetApi:
    """
    API class for data set CRUD operations.
    """

    def __init__(self, config: ClientConfig, use_json: bool = False):
        self.client = (DataSetHttpClient if use_json else DataSetGrpcClient)(config)

    def list_data_sets(self) -> Sequence[DataSet]:
        """
        List all data sets.
        """
        response = self.client.list_data_sets(ListDataSetsRequest())
        return [DataSet.from_proto(d) for d in response.data_sets]

    def get_data_set(self, name: str) -> Optional[DataSet]:
        """
        Get one data set.

        Return None if the data set does not exist.

        Args:
            name:   The resource name of the requested data set, for example
                    "dataSet/123".
        """
        try:
            response = self.client.get_data_set(GetDataSetRequest(name=name))
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise
        return DataSet.from_proto(response)

    def create_data_set(self, data_set: DataSet) -> DataSet:
        """
        Create a data set.

        Args:
            data_set: The data set to create.
        """
        response = self.client.create_data_set(CreateDataSetRequest(data_set=data_set.to_proto()))
        return DataSet.from_proto(response)

    def update_data_set(
        self,
        data_set: DataSet,
        update_mask: FieldMask = None,
        allow_missing: bool = False,
    ) -> DataSet:
        """
        Update a data set.

        Args:
            data_set:       The data set to update.
            update_mask:    The fields to update. If not specified, the update behaves as a
                            full update, overwriting all existing fields and properties.
            allow_missing:  If set to true, and the resource is not found, a new resource will be
                            created. In this situation, the "update_mask" is ignored.
        """
        response = self.client.update_data_set(
            UpdateDataSetRequest(
                data_set=data_set.to_proto(),
                update_mask=update_mask,
                allow_missing=allow_missing,
            )
        )
        return DataSet.from_proto(response)

    def delete_data_set(self, data_set: str) -> None:
        """
        Delete a data set.

        Args:
            data_set: The data set to delete.
        """
        self.client.delete_data_set(DeleteDataSetRequest(name=data_set))
