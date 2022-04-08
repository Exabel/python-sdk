from exabel_data_sdk.client.api.data_classes.group import Group
from exabel_data_sdk.stubs.exabel.api.management.v1.all_pb2 import (
    FolderAccessor as ProtoFolderAccessor,
)


class FolderAccessor:
    """
    An accessor of a folder.

    Attributes:
        group (Group):  A group.
        write (bool):   Whether the group has write access. Read access is implied.
    """

    def __init__(self, group: Group, write: bool):
        """
        Create a FolderAccessor.

        Args:
            group (Group):  A group.
            write (bool):   Whether the group has write access. Read access is implied.
        """
        self.group = group
        self.write = write

    @staticmethod
    def from_proto(folder_accessor: ProtoFolderAccessor) -> "FolderAccessor":
        """Create a FolderAccessor from the given protobuf FolderAccessor."""
        return FolderAccessor(
            group=Group.from_proto(folder_accessor.group), write=folder_accessor.write
        )

    def to_proto(self) -> ProtoFolderAccessor:
        """Create a proto FolderAccessor from this FolderAccessor."""
        return ProtoFolderAccessor(
            group=self.group.to_proto(),
            write=self.write,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FolderAccessor):
            return False
        return self.group == other.group and self.write == other.write

    def __repr__(self) -> str:
        return f"FolderAccessor(group='{self.group}', write={self.write})"
