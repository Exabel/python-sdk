import copy
from datetime import datetime

from dateutil import tz

from exabel.client.api.data_classes.folder import Folder
from exabel.client.api.data_classes.folder_item import FolderItem, FolderItemType


class TestFolder:
    def test_proto_conversion(self):
        folder = Folder(
            name="folders/123",
            display_name="My Folder",
            write=True,
            items=[
                FolderItem(
                    parent="folders/123",
                    name="predictionModels/123",
                    display_name="My prediction model",
                    item_type=FolderItemType.PREDICTION_MODEL,
                    description="A description of the prediction model",
                    create_time=datetime(2022, 3, 3, tzinfo=tz.tzutc()),
                    update_time=datetime(2022, 4, 2, tzinfo=tz.tzutc()),
                    created_by="users/123",
                    updated_by="users/234",
                )
            ],
        )
        assert folder == Folder.from_proto(folder.to_proto())

    def test_equals(self):
        folder_1 = Folder(
            name="folders/123",
            display_name="My Folder",
            write=True,
            items=[
                FolderItem(
                    parent="folders/123",
                    name="predictionModels/123",
                    display_name="My prediction model",
                    item_type=FolderItemType.PREDICTION_MODEL,
                    description="A description of the prediction model",
                    create_time=datetime(2022, 3, 3, tzinfo=tz.tzutc()),
                    update_time=datetime(2022, 4, 2, tzinfo=tz.tzutc()),
                    created_by="users/123",
                    updated_by="users/234",
                )
            ],
        )
        folder_2 = Folder(
            name="folders/123",
            display_name="My Folder",
            write=True,
            items=[],
        )
        assert folder_1 == copy.copy(folder_1)
        assert folder_1 != folder_2
