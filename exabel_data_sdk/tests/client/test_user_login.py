import unittest

from exabel_data_sdk.client.user_login import UserLogin


class TestUserLogin(unittest.TestCase):
    def test_reauthenticate(self):
        user_login = UserLogin(reauthenticate=True)
        self.assertTrue(user_login.reauthenticate)
        user_login.get_access_token()
        self.assertFalse(user_login.reauthenticate)
