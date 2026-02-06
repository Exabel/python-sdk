import argparse
import unittest

import pytest

from exabel.scripts.export_data import ExportData


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
            "--retries",
            "2",
        ]

    def _assert_common_args(self, args: argparse.Namespace):
        assert args.query == "query"
        assert args.filename == "filename"
        assert args.format == "format"
        assert args.retries == 2

    def test_args__api_key(self):
        script = ExportData(self.common_args + ["--api-key", "api-key"], "Export")
        args = script.parse_arguments()
        self._assert_common_args(args)
        assert args.api_key == "api-key"

    def test_args__access_token(self):
        script = ExportData(self.common_args + ["--access-token", "access-token"], "Export")
        args = script.parse_arguments()
        self._assert_common_args(args)
        assert args.access_token == "access-token"

    def test_args__neither_api_key_nor_access_token_should_fail(self):
        script = ExportData(self.common_args, "Export")
        with pytest.raises(SystemExit):
            script.parse_arguments()

    def test_args__both_api_key_and_access_token_should_fail(self):
        script = ExportData(
            self.common_args + ["--api-key", "api-key", "--access-token", "access-token"],
            "Export",
        )
        with pytest.raises(SystemExit):
            script.parse_arguments()
