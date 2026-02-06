import copy

from exabel.client.api.data_classes.folder_accessor import FolderAccessor
from exabel.client.api.data_classes.group import Group


class TestFolderAccessor:
    def test_proto_conversion(self):
        folder_accessor = FolderAccessor(
            group=Group(name="groups/123", display_name="My group", users=[]), write=True
        )
        assert folder_accessor == FolderAccessor.from_proto(folder_accessor.to_proto())

    def test_equals(self):
        folder_accessor_1 = FolderAccessor(
            group=Group(name="groups/123", display_name="My group", users=[]), write=True
        )
        folder_accessor_2 = FolderAccessor(
            group=Group(name="groups/12", display_name="My group", users=[]), write=True
        )
        assert folder_accessor_1 == copy.copy(folder_accessor_1)
        assert folder_accessor_1 != folder_accessor_2
