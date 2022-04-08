import unittest

from exabel_data_sdk.client.api.data_classes.group import Group
from exabel_data_sdk.client.api.data_classes.user import User


class TestDataSet(unittest.TestCase):
    def test_proto_conversion(self):
        group = Group(
            name="groups/123",
            display_name="My Group",
            users=[User(name="users/123", email="example@example.com", blocked=False)],
        )
        self.assertEqual(group, Group.from_proto(group.to_proto()))

    def test_equals(self):
        group_1 = Group(
            name="groups/123",
            display_name="My Group",
            users=[
                User(name="users/1", email="example@example.com", blocked=False),
                User(name="users/2", email="example@example.com", blocked=False),
            ],
        )
        group_2 = Group(
            name="groups/123",
            display_name="My Group",
            users=[],
        )

        group_3 = Group(
            name="groups/123",
            display_name="My Group",
            users=[
                User(name="users/2", email="example@example.com", blocked=False),
                User(name="users/1", email="example@example.com", blocked=False),
            ],
        )
        self.assertEqual(group_1, group_3)
        self.assertNotEqual(group_1, group_2)
