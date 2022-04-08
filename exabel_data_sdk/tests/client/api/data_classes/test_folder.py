import unittest
from datetime import datetime

from dateutil import tz

from exabel_data_sdk.client.api.data_classes.folder import Folder
from exabel_data_sdk.client.api.data_classes.folder_item import FolderItem, FolderItemType


class TestFolder(unittest.TestCase):
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
                    create_time=datetime(2022, 3, 3, tzinfo=tz.tzutc()),
                    update_time=datetime(2022, 4, 2, tzinfo=tz.tzutc()),
                    created_by="users/123",
                    updated_by="users/234",
                )
            ],
        )
        self.assertEqual(folder, Folder.from_proto(folder.to_proto()))

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
        self.assertEqual(folder_1, folder_1)
        self.assertNotEqual(folder_1, folder_2)
