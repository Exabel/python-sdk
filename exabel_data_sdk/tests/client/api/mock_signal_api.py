from typing import Optional

from google.protobuf.field_mask_pb2 import FieldMask

from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.api.signal_api import SignalApi
from exabel_data_sdk.tests.client.api.mock_resource_store import MockResourceStore


# pylint: disable=super-init-not-called
class MockSignalApi(SignalApi):
    """
    Mock of the EntityApi class for CRUD operations on entities and entity types.
    """

    def __init__(self):
        self.signals = MockResourceStore()
        self.created_library_signals = []

    def list_signals(self, page_size: int = 1000, page_token: str = None) -> PagingResult[Signal]:
        return self.signals.list()

    def get_signal(self, name: str) -> Optional[Signal]:
        return self.signals.get(name)

    def create_signal(self, signal: Signal, create_library_signal: bool = False) -> Signal:
        if create_library_signal:
            self.created_library_signals.append(signal)
        return self.signals.create(signal)

    def update_signal(
        self,
        signal: Signal,
        update_mask: FieldMask = None,
        allow_missing: bool = False,
        create_library_signal: bool = False,
    ) -> Signal:
        return self.signals.update(signal, allow_missing=allow_missing)

    def delete_signal(self, name: str) -> None:
        self.signals.delete(name)
