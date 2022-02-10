from typing import Optional

from google.protobuf.field_mask_pb2 import FieldMask

from exabel_data_sdk.client.api.api_client.grpc.signal_grpc_client import SignalGrpcClient
from exabel_data_sdk.client.api.api_client.http.signal_http_client import SignalHttpClient
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateSignalRequest,
    DeleteSignalRequest,
    GetSignalRequest,
    ListSignalsRequest,
    UpdateSignalRequest,
)


class SignalApi:
    """
    API class for Signal CRUD operations.
    """

    def __init__(self, config: ClientConfig, use_json: bool):
        self.client = (SignalHttpClient if use_json else SignalGrpcClient)(config)

    def list_signals(self, page_size: int = 1000, page_token: str = None) -> PagingResult[Signal]:
        """
        List all signals.

        Args:
            page_size:      The maximum number of results to return.
                            Defaults to 1000, which is also the maximum size of this field.
            page_token:     The page token to resume the results from.
        """
        response = self.client.list_signals(
            ListSignalsRequest(page_size=page_size, page_token=page_token)
        )
        return PagingResult(
            results=[Signal.from_proto(t) for t in response.signals],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    def get_signal(self, name: str) -> Optional[Signal]:
        """
        Get one signal.

        Return None if the signal does not exist.

        Args:
            name: The resource name of the requested signal, for example "signals/ns.signal1".
        """
        try:
            response = self.client.get_signal(
                GetSignalRequest(name=name),
            )
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise
        return Signal.from_proto(response)

    def create_signal(self, signal: Signal, create_library_signal: bool = False) -> Signal:
        """
        Create one signal and returns it.

        Args:
            signal: The signal to create.
            create_library_signal: Set to true to add the signal to the library when created.
        """
        response = self.client.create_signal(
            CreateSignalRequest(
                signal=signal.to_proto(), create_library_signal=create_library_signal
            ),
        )
        return Signal.from_proto(response)

    def update_signal(
        self,
        signal: Signal,
        update_mask: FieldMask = None,
        allow_missing: bool = False,
        create_library_signal: bool = False,
    ) -> Signal:
        """
        Update one signal and return it.

        Args:
            signal:         The signal to update.
            update_mask:    The fields to update. If not specified, the update behaves as a
                            full update, overwriting all existing fields and properties.
            allow_missing:  If set to true, and the resource is not found, a new resource will be
                            created. In this situation, the "update_mask" is ignored.
            create_library_signal:
                            If allow_missing is set to true and the signal does not exist, also add
                            it to the library.
        """
        response = self.client.update_signal(
            UpdateSignalRequest(
                signal=signal.to_proto(),
                update_mask=update_mask,
                allow_missing=allow_missing,
                create_library_signal=create_library_signal,
            ),
        )
        return Signal.from_proto(response)

    def delete_signal(self, name: str) -> None:
        """
        Delete one signal.

        All time series for this signal will also be deleted.

        Args:
            name: The resource name of the signal to delete, for example "signals/ns.signal1".
        """
        self.client.delete_signal(
            DeleteSignalRequest(name=name),
        )
