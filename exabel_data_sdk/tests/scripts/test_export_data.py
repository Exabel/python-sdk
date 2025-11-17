import argparse
import unittest
from unittest import mock

from exabel_data_sdk.scripts.export_data import ExportData


class TestExportData(unittest.TestCase):
    def setUp(self):
        self.common_args = [
            "script",
            "--query",
            "query",
            "--filename",
            "filename",
            "--format",
            "format",
            "--use-test-backend",
        ]

    def _assert_common_args(self, args: argparse.Namespace):
        self.assertEqual(args.query, "query")
        self.assertEqual(args.filename, "filename")
        self.assertEqual(args.format, "format")
        self.assertTrue(args.use_test_backend)

    def test_args__api_key(self):
        script = ExportData(self.common_args + ["--api-key", "api-key"])
        args = script.parse_arguments()
        self._assert_common_args(args)
        self.assertEqual(args.api_key, "api-key")

    def test_args__access_token(self):
        script = ExportData(self.common_args + ["--access-token", "access-token"])
        args = script.parse_arguments()
        self._assert_common_args(args)
        self.assertEqual(args.access_token, "access-token")

    def test_args__reauthenticate(self):
        script = ExportData(self.common_args + ["--reauthenticate"])
        args = script.parse_arguments()
        self._assert_common_args(args)
        self.assertTrue(args.reauthenticate)

    def test_args__defaults(self):
        script = ExportData(self.common_args)
        args = script.parse_arguments()
        self._assert_common_args(args)
        self.assertFalse(args.reauthenticate)

    def test_description_optional(self):
        # To maintain backwards compatibility
        script = ExportData(self.common_args)
        self.assertIsNotNone(script.parser.description)

    def test_description(self):
        script = ExportData(self.common_args, "Export")
        self.assertEqual(script.parser.description, "Export")

    def test_args__both_api_key_and_reauthenticate_should_fail(self):
        script = ExportData(self.common_args + ["--api-key", "api-key", "--reauthenticate"])
        with self.assertRaises(SystemExit):
            script.parse_arguments()

    def test_args__both_api_key_and_access_token_should_fail(self):
        script = ExportData(
            self.common_args + ["--api-key", "api-key", "--access-token", "access-token"]
        )
        with self.assertRaises(SystemExit):
            script.parse_arguments()

    @mock.patch("exabel_data_sdk.client.api.export_api.ExportApi.from_api_key")
    def test_get_export_api_from_api_key(self, from_api_key_mock):
        """Factory method ExportApi.use_api_key should be called is api-key not None."""
        ExportData.get_export_api(api_key="api-key", retries=2)
        from_api_key_mock.assert_called_with("api-key", False, retries=2)
        ExportData.get_export_api(api_key="api-key", use_test_backend=True)
        from_api_key_mock.assert_called_with("api-key", True, retries=0)

    @mock.patch("exabel_data_sdk.client.api.export_api.ExportApi.from_access_token")
    def test_get_export_api_from_access_token(self, from_access_token_mock):
        """Factory method ExportApi.use_api_key should be called is api-key not None."""
        ExportData.get_export_api(access_token="access-token", retries=2)
        from_access_token_mock.assert_called_with("access-token", False, retries=2)
        ExportData.get_export_api(access_token="access-token", use_test_backend=True)
        from_access_token_mock.assert_called_with("access-token", True, retries=0)
