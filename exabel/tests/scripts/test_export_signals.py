import argparse
import os
import unittest

import pandas as pd
import pytest

from exabel.scripts.export_signals import ExportSignals


class TestExportSignals(unittest.TestCase):
    def setUp(self):
        self.common_args = [
            "script",
            "--signal",
            "signalA",
            "expression() AS signalB",
            "--tag",
            "rbics:5010",
            "rbics:5012",
            "--start-date",
            "2023-01-31",
            "--end-date",
            "2024-02-29",
            "--filename",
        ]

    def _assert_common_args(self, args: argparse.Namespace):
        assert args.signal == ["signalA", "expression() AS signalB"]
        assert args.tag == ["rbics:5010", "rbics:5012"]
        assert args.start_date == pd.Timestamp("2023-01-31")
        assert args.end_date == pd.Timestamp("2024-02-29")

    def test_args_api_key(self):
        script = ExportSignals(self.common_args + ["foo.csv", "--api-key", "api-key"], "desc")
        assert script.parser.description == "desc"
        args = script.parse_arguments()
        self._assert_common_args(args)
        assert args.filename == "foo.csv"
        assert args.api_key == "api-key"

    def test_args_env_variable(self):
        os.environ["EXABEL_API_KEY"] = "env_key"
        try:
            script = ExportSignals(self.common_args + ["foo.csv"], "desc")
            assert script.parser.description == "desc"
            args = script.parse_arguments()
            self._assert_common_args(args)
            assert args.api_key is None
            assert args.filename == "foo.csv"
        finally:
            del os.environ["EXABEL_API_KEY"]

    def test_args_known_time(self):
        script = ExportSignals(
            self.common_args + ["foo.csv", "--api-key", "api-key", "--known-time", "2024-01-03"],
            "desc",
        )
        assert script.parser.description == "desc"
        args = script.parse_arguments()
        self._assert_common_args(args)
        assert args.known_time == pd.Timestamp("2024-01-03")

    def test_args_missing_api_key(self):
        script = ExportSignals(self.common_args + ["foo.csv"], "desc")
        with pytest.raises(SystemExit):
            script.parse_arguments()

    def test_args_unknown_file_extension(self):
        script = ExportSignals(self.common_args + ["foo.pdf", "--api-key", "api-key"], "desc")
        with pytest.raises(SystemExit):
            script.parse_arguments()

    def test_args_unknown_date_format(self):
        script = ExportSignals(
            self.common_args + ["foo.pickle", "--api-key", "api-key", "--known-time", "Monday"],
            "desc",
        )
        with pytest.raises(SystemExit):
            script.parse_arguments()
