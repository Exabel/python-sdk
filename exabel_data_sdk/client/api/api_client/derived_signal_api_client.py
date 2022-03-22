from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    CreateDerivedSignalRequest,
    DeleteDerivedSignalRequest,
    DerivedSignal,
    GetDerivedSignalRequest,
    UpdateDerivedSignalRequest,
)


class DerivedSignalApiClient(ABC):
    """
    Superclass for clients that send derived signal requests to the Exabel Analytics API.
    """

    @abstractmethod
    def create_derived_signal(self, request: CreateDerivedSignalRequest) -> DerivedSignal:
        """Create a derived signal."""

    @abstractmethod
    def get_derived_signal(self, request: GetDerivedSignalRequest) -> DerivedSignal:
        """Get a derived signal."""

    @abstractmethod
    def update_derived_signal(self, request: UpdateDerivedSignalRequest) -> DerivedSignal:
        """Update a derived signal."""

    @abstractmethod
    def delete_derived_signal(self, request: DeleteDerivedSignalRequest) -> None:
        """Delete a derived signal."""
