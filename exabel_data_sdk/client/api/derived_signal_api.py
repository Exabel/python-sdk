from typing import Optional

from exabel_data_sdk.client.api.api_client.grpc.derived_signal_grpc_client import (
    DerivedSignalGrpcClient,
)
from exabel_data_sdk.client.api.api_client.http.derived_signal_http_client import (
    DerivedSignalHttpClient,
)
from exabel_data_sdk.client.api.data_classes.derived_signal import DerivedSignal
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    CreateDerivedSignalRequest,
    DeleteDerivedSignalRequest,
    GetDerivedSignalRequest,
    UpdateDerivedSignalRequest,
)


class DerivedSignalApi:
    """
    API class for derived signal CRUD operations.
    """

    def __init__(self, config: ClientConfig, use_json: bool = False):
        self.client = (DerivedSignalHttpClient if use_json else DerivedSignalGrpcClient)(config)

    def create_derived_signal(self, signal: DerivedSignal, folder: str = None) -> DerivedSignal:
        """
        Create a derived signal.

        Args:
            signal: The derived signal to create.
            folder: The resource name of the folder to put the signal in. Example: "folders/123".
                    If not provided, the signal will be put in the default analytics API folder.
        """
        response = self.client.create_derived_signal(
            CreateDerivedSignalRequest(signal=signal.to_proto(), folder=folder)
        )
        return DerivedSignal.from_proto(response)

    def get_derived_signal(self, name: str) -> Optional[DerivedSignal]:
        """
        Get a derived signal.

        Return None if the signal does not exist.

        Args:
            name:   The resource name of the derived signal, for example "derivedSignals/123".
        """
        try:
            response = self.client.get_derived_signal(GetDerivedSignalRequest(name=name))
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise
        return DerivedSignal.from_proto(response)

    def update_derived_signal(self, signal: DerivedSignal) -> DerivedSignal:
        """
        Update a derived signal.

        Args:
            signal: The derived signal to update.
        """
        response = self.client.update_derived_signal(
            UpdateDerivedSignalRequest(signal=signal.to_proto())
        )
        return DerivedSignal.from_proto(response)

    def delete_derived_signal(self, name: str) -> None:
        """
        Delete a derived signal.

        Args:
            name:   The resource name of the derived signal, for example "derivedSignals/123".
        """
        self.client.delete_derived_signal(DeleteDerivedSignalRequest(name=name))
