from exabel_data_sdk.client.api.base_api import BaseApi
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateSignalRequest,
    DeleteSignalRequest,
    GetSignalRequest,
    ListSignalsRequest,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2_grpc import SignalServiceStub


class SignalApi(BaseApi):
    """
    API class for Signal CRUD operations.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        self.stub = SignalServiceStub(self.channel)

    @handle_grpc_error
    def list_signals(self, page_size: int = 1000, page_token: str = None) -> PagingResult[Signal]:
        """
        List all signals.

        Args:
            page_size:      The maximum number of results to return.
                            Defaults to 1000, which is also the maximum size of this field.
            page_token:     The page token to resume the results from.
        """
        response = self.stub.ListSignals(
            ListSignalsRequest(page_size=page_size, page_token=page_token),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return PagingResult(
            results=[Signal.from_proto(t) for t in response.signals],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    @handle_grpc_error
    def get_signal(self, name: str) -> Signal:
        """
        Get one signal.

        Args:
            name: The resource name of the requested signal, for example "signals/ns.signal1".
        """
        response = self.stub.GetSignal(
            GetSignalRequest(name=name),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return Signal.from_proto(response)

    @handle_grpc_error
    def create_signal(self, signal: Signal) -> Signal:
        """
        Create one signal and returns it.

        Args:
            signal: The signal to create.
        """
        response = self.stub.CreateSignal(
            CreateSignalRequest(signal=signal.to_proto()),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return Signal.from_proto(response)

    @handle_grpc_error
    def delete_signal(self, name: str) -> None:
        """
        Delete one signal.

        All time series for this signal will also be deleted.

        Args:
            name: The resource name of the signal to delete, for example "signals/ns.signal1".
        """
        self.stub.DeleteSignal(
            DeleteSignalRequest(name=name),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
