from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateSignalRequest,
    DeleteSignalRequest,
    GetSignalRequest,
    ListSignalsRequest,
    ListSignalsResponse,
    Signal,
)


class SignalApiClient(ABC):
    """
    Superclass for clients that send signal requests to the Exabel Data API.
    """

    @abstractmethod
    def list_signals(self, request: ListSignalsRequest) -> ListSignalsResponse:
        """List all signals."""

    @abstractmethod
    def get_signal(self, request: GetSignalRequest) -> Signal:
        """Get a signal."""

    @abstractmethod
    def create_signal(self, request: CreateSignalRequest) -> Signal:
        """Create a signal."""

    @abstractmethod
    def delete_signal(self, request: DeleteSignalRequest) -> None:
        """Delete a signal."""
