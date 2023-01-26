import json
import unittest
from unittest import mock

from exabel_data_sdk.client.user_login import RefreshTokens, UserLogin


class TestUserLogin(unittest.TestCase):
    def test_reauthenticate(self):
        user_login = UserLogin(reauthenticate=True)
        self.assertTrue(user_login.reauthenticate)
        user_login.get_access_token()
        self.assertFalse(user_login.reauthenticate)

    @mock.patch("os.path.isfile", return_value=True)
    def test_convert_old_refresh_token_file(self, _):
        user_login = UserLogin()
        with mock.patch("builtins.open", mock.mock_open(read_data="token")) as mock_open:
            user_login.read_refresh_token()
        self.assertEqual(
            user_login.tokens,
            RefreshTokens({"endpoints.exabel.com": {"__default__": "token"}}),
        )
        write_arg = mock_open.return_value.__enter__.return_value.write.call_args[0][0]
        self.assertEqual(
            {"endpoints.exabel.com": {"__default__": "token"}},
            json.loads(write_arg),
        )

    @mock.patch("os.path.isfile", return_value=True)
    def test_refresh_token(self, _):
        user_login = UserLogin(user="user")
        token_file_content = json.dumps({"endpoints.exabel.com": {"user": "token"}})
        with mock.patch("builtins.open", mock.mock_open(read_data=token_file_content)):
            user_login.read_refresh_token()
        self.assertEqual(
            user_login.refresh_token,
            "token",
        )

    @mock.patch("os.path.isfile", return_value=True)
    def test_refresh_token__default_user(self, _):
        user_login = UserLogin()
        token_file_content = json.dumps({"endpoints.exabel.com": {"__default__": "token"}})
        with mock.patch("builtins.open", mock.mock_open(read_data=token_file_content)):
            user_login.read_refresh_token()
        self.assertEqual(
            user_login.refresh_token,
            "token",
        )


class TestRefreshTokens(unittest.TestCase):
    def test_refresh_token_file(self):
        host_tokens = {"host1": {"user1": "token1"}, "host2": {"user2": "token2"}}
        tokens = RefreshTokens(host_tokens)
        self.assertEqual("token1", tokens.get_refresh_token("host1", "user1"))
        self.assertEqual("token2", tokens.get_refresh_token("host2", "user2"))
        self.assertEqual("", tokens.get_refresh_token("unknown_host", "anything"))
        self.assertEqual("", tokens.get_refresh_token("host1", "unknown_user"))

    def test_invalid_host_tokens_should_fail(self):
        with self.assertRaises(ValueError):
            RefreshTokens([])
        with self.assertRaises(ValueError):
            RefreshTokens({"host": "token"})
        with self.assertRaises(ValueError):
            RefreshTokens({"host": {"user": 1}})
        with self.assertRaises(ValueError):
            RefreshTokens({"host": []})

    def test_merge_with(self):
        host_tokens = {"host1": {"user1": "token1"}, "host2": {"user2": "token2"}}
        tokens = RefreshTokens(host_tokens)
        merged_tokens = tokens.merge_with(
            RefreshTokens({"host1": {"user3": "token3"}, "host3": {"user4": "token4"}})
        )
        self.assertEqual("token1", merged_tokens.get_refresh_token("host1", "user1"))
        self.assertEqual("token3", merged_tokens.get_refresh_token("host1", "user3"))
        self.assertEqual("token2", merged_tokens.get_refresh_token("host2", "user2"))
        self.assertEqual("token4", merged_tokens.get_refresh_token("host3", "user4"))

    def test_merge_with__overwrites(self):
        host_tokens = {"host": {"user": "token"}}
        tokens = RefreshTokens(host_tokens)
        merged_token_file = tokens.merge_with(RefreshTokens({"host": {"user": "new_token"}}))
        self.assertEqual("new_token", merged_token_file.get_refresh_token("host", "user"))

    def test_from_token(self):
        tokens = RefreshTokens.from_host_user_token("host", "user", "token")
        self.assertEqual("token", tokens.get_refresh_token("host", "user"))

    def test_from_host_and_user(self):
        tokens = RefreshTokens.from_host_user("host", "user")
        self.assertEqual("", tokens.get_refresh_token("host", "user"))

    def test_to_json(self):
        host_tokens = {"host1": {"user1": "token1"}, "host2": {"user2": "token2"}}
        tokens = RefreshTokens(host_tokens)
        self.assertEqual(
            json.dumps(host_tokens, indent=4),
            tokens.to_json(),
        )

    def test_from_json(self):
        host_tokens = {"host1": {"user1": "token1"}, "host2": {"user2": "token2"}}
        tokens = RefreshTokens(host_tokens)
        self.assertEqual(
            tokens,
            RefreshTokens.from_json(tokens.to_json()),
        )
