import unittest
from datetime import datetime

from dateutil import tz

from exabel_data_sdk.client.api.data_classes.folder_item import FolderItem, FolderItemType


class TestFolderItem(unittest.TestCase):
    def test_proto_conversion(self):
        folder_item = FolderItem(
            parent="folders/123",
            name="predictionModels/123",
            display_name="My prediction model",
            item_type=FolderItemType.PREDICTION_MODEL,
            create_time=datetime(2022, 3, 3, tzinfo=tz.tzutc()),
            update_time=datetime(2022, 4, 2, tzinfo=tz.tzutc()),
            created_by="users/123",
            updated_by="users/234",
        )
        self.assertEqual(folder_item, FolderItem.from_proto(folder_item.to_proto()))

    def test_proto_conversion__item_without_created_and_updated_by(self):
        folder_item = FolderItem(
            parent="folders/123",
            name="predictionModels/123",
            display_name="My prediction model",
            item_type=FolderItemType.PREDICTION_MODEL,
            create_time=datetime(2022, 3, 3, tzinfo=tz.tzutc()),
            update_time=datetime(2022, 4, 2, tzinfo=tz.tzutc()),
            created_by=None,
            updated_by=None,
        )
        self.assertEqual(folder_item, FolderItem.from_proto(folder_item.to_proto()))

    def test_equals(self):
        folder_item_1 = FolderItem(
            parent="folders/123",
            name="predictionModels/123",
            display_name="My prediction model",
            item_type=FolderItemType.PREDICTION_MODEL,
            create_time=datetime(2022, 3, 3, tzinfo=tz.tzutc()),
            update_time=datetime(2022, 4, 2, tzinfo=tz.tzutc()),
            created_by="users/123",
            updated_by="users/234",
        )
        folder_item_2 = FolderItem(
            parent="folders/123",
            name="predictionModels/123",
            display_name="My prediction model",
            item_type=FolderItemType.PREDICTION_MODEL,
            create_time=datetime(2022, 3, 3, tzinfo=tz.tzutc()),
            update_time=datetime(2022, 4, 2, tzinfo=tz.tzutc()),
            created_by="users/123",
            updated_by="users/234",
        )
        folder_item_3 = FolderItem(
            parent="folders/123",
            name="derivedSignals/123",
            display_name="signal",
            item_type=FolderItemType.DERIVED_SIGNAL,
            create_time=datetime(2022, 3, 3, tzinfo=tz.tzutc()),
            update_time=datetime(2022, 4, 2, tzinfo=tz.tzutc()),
            created_by="users/123",
            updated_by="users/234",
        )
        self.assertEqual(folder_item_1, folder_item_2)
        self.assertNotEqual(folder_item_1, folder_item_3)
