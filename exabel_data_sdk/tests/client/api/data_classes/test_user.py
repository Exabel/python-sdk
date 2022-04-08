import unittest

from exabel_data_sdk.client.api.data_classes.user import User


class TestUser(unittest.TestCase):
    def test_proto_conversion(self):
        user = User(name="users/123", email="example@example.com", blocked=False)
        self.assertEqual(user, User.from_proto(user.to_proto()))

    def test_equals(self):
        user_1 = User(name="users/1", email="example@example.com", blocked=False)
        user_2 = User(name="users/2", email="example@example.com", blocked=False)
        self.assertEqual(user_1, user_1)
        self.assertNotEqual(user_1, user_2)
