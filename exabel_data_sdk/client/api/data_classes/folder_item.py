from datetime import datetime
from enum import Enum
from typing import Optional

from dateutil import tz
from google.protobuf.timestamp_pb2 import Timestamp as ProtoTimestamp

from exabel_data_sdk.stubs.exabel.api.management.v1.all_pb2 import FolderItem as ProtoFolderItem
from exabel_data_sdk.stubs.exabel.api.management.v1.all_pb2 import (
    FolderItemType as ProtoFolderItemType,
)


class FolderItemType(Enum):
    """Enum representing the type of a folder item."""

    # Derived signal.
    DERIVED_SIGNAL = ProtoFolderItemType.DERIVED_SIGNAL
    # Prediction model.
    PREDICTION_MODEL = ProtoFolderItemType.PREDICTION_MODEL
    # Portfolio strategy.
    PORTFOLIO_STRATEGY = ProtoFolderItemType.PORTFOLIO_STRATEGY
    # Dashboard.
    DASHBOARD = ProtoFolderItemType.DASHBOARD
    # Entity drill down view.
    DRILL_DOWN = ProtoFolderItemType.DRILL_DOWN
    # Static tag.
    TAG = ProtoFolderItemType.TAG
    # Screen.
    SCREEN = ProtoFolderItemType.SCREEN


class FolderItem:
    """
    A folder item resource in the Management API.

    Attributes:
        parent (str):           Parent folder resource name. Example "folders/123".
        name (str):             Folder item resource name. Example: "derivedSignals/123".
        display_name (str):     Display name of the folder item.
        item_type (str):        Type of the folder item.
        create_time (datetime): Time the item was created.
        update_time (datetime): Time the item was last updated.
        created_by (str):       Resource name of the user who created the item.
        updated_by (str):       Resource name of the user who last updated the item.
    """

    def __init__(
        self,
        parent: str,
        name: str,
        display_name: str,
        item_type: FolderItemType,
        create_time: datetime,
        update_time: datetime,
        created_by: Optional[str],
        updated_by: Optional[str],
    ):
        """
        Create a FolderItem.

        Args:
            parent (str):           Parent folder resource name. Example "folders/123".
            name (str):             Folder item resource name. Example: "derivedSignals/123".
            display_name (str):     Display name of the folder item.
            item_type (str):        Type of the folder item.
            create_time (datetime): Time the item was created.
            update_time (datetime): Time the item was last updated.
            created_by (str):       Resource name of the user who created the item.
            updated_by (str):       Resource name of the user who last updated the item.
        """
        self.parent = parent
        self.name = name
        self.display_name = display_name
        self.item_type = item_type
        self.create_time = create_time
        self.update_time = update_time
        self.created_by = created_by
        self.updated_by = updated_by

    @classmethod
    def from_proto(cls, folder_item: ProtoFolderItem) -> "FolderItem":
        """Create a FolderItem from the given protobuf FolderItem."""
        return FolderItem(
            parent=folder_item.parent,
            name=folder_item.name,
            display_name=folder_item.display_name,
            item_type=FolderItemType(folder_item.item_type),
            create_time=cls._proto_timestamp_to_datetime(folder_item.create_time),
            update_time=cls._proto_timestamp_to_datetime(folder_item.update_time),
            created_by=folder_item.created_by or None,
            updated_by=folder_item.updated_by or None,
        )

    def to_proto(self) -> ProtoFolderItem:
        """Create a proto FolderItem from this FolderItem."""
        return ProtoFolderItem(
            parent=self.parent,
            name=self.name,
            display_name=self.display_name,
            item_type=self.item_type.value,
            create_time=self._datetime_to_proto_timestamp(self.create_time),
            update_time=self._datetime_to_proto_timestamp(self.update_time),
            created_by=self.created_by,
            updated_by=self.updated_by,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FolderItem):
            return False
        return (
            self.parent == other.parent
            and self.name == other.name
            and self.display_name == other.display_name
            and self.item_type == other.item_type
            and self.create_time == other.create_time
            and self.update_time == other.update_time
            and self.created_by == other.created_by
            and self.updated_by == other.updated_by
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, FolderItem):
            raise ValueError(f"Cannot compare FolderItem to non-FolderItem: {other}")
        return self.name < other.name

    def __repr__(self) -> str:
        return (
            f"FolderItem(parent='{self.parent}', name='{self.name}', "
            f"display_name='{self.display_name}', item_type={self.item_type}, "
            f"create_time={self.create_time}, update_time={self.update_time}, "
            f"created_by={self.created_by}, updated_by={self.updated_by})"
        )

    @staticmethod
    def _proto_timestamp_to_datetime(timestamp: ProtoTimestamp) -> datetime:
        return datetime.fromtimestamp(timestamp.seconds, tz=tz.tzutc())

    @staticmethod
    def _datetime_to_proto_timestamp(date: datetime) -> ProtoTimestamp:
        timestamp = ProtoTimestamp()
        timestamp.seconds = int(date.timestamp())
        return timestamp
