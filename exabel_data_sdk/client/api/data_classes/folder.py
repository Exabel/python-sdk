from typing import Sequence

from exabel_data_sdk.client.api.data_classes.folder_item import FolderItem
from exabel_data_sdk.stubs.exabel.api.management.v1.all_pb2 import Folder as ProtoFolder


class Folder:
    """
    A folder resource in the Management API.

    Attributes:
        name (str):         The resource name of the folder, for example "folders/123".
        display_name (str): The display name of the folder.
        write (bool):       Whether the caller has write access to the folder.
        items (list):       The items in the folder.
    """

    def __init__(self, name: str, display_name: str, write: bool, items: Sequence[FolderItem]):
        """
        Create a Folder.

        Args:
            name (str):         The resource name of the folder, for example "folders/123".
            display_name (str): The display name of the folder.
            write (bool):       Whether the caller has write access to the folder.
            items (list):       The items in the folder.
        """
        self.name = name
        self.display_name = display_name
        self.write = write
        self.items = items

    @staticmethod
    def from_proto(folder: ProtoFolder) -> "Folder":
        """Create a Folder from the given protobuf Folder."""
        return Folder(
            name=folder.name,
            display_name=folder.display_name,
            write=folder.write,
            items=[FolderItem.from_proto(item) for item in folder.items],
        )

    def to_proto(self) -> ProtoFolder:
        """Create a proto Folder from this Folder."""
        return ProtoFolder(
            name=self.name,
            display_name=self.display_name,
            write=self.write,
            items=[item.to_proto() for item in self.items],
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Folder):
            return False
        return (
            self.name == other.name
            and self.display_name == other.display_name
            and self.write == other.write
            and sorted(self.items) == sorted(other.items)
        )

    def __repr__(self) -> str:
        return (
            f"Folder(name='{self.name}', display_name='{self.display_name}', "
            f"write={self.write}, items={self.items})"
        )
