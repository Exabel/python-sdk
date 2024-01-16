import argparse
import os
import unittest

import pandas as pd

from exabel_data_sdk.scripts.export_signals import ExportSignals


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
        self.assertEqual(args.signal, ["signalA", "expression() AS signalB"])
        self.assertEqual(args.tag, ["rbics:5010", "rbics:5012"])
        self.assertEqual(args.start_date, pd.Timestamp("2023-01-31"))
        self.assertEqual(args.end_date, pd.Timestamp("2024-02-29"))

    def test_args_api_key(self):
        script = ExportSignals(self.common_args + ["foo.csv", "--api-key", "api-key"], "desc")
        self.assertEqual(script.parser.description, "desc")
        args = script.parse_arguments()
        self._assert_common_args(args)
        self.assertEqual(args.filename, "foo.csv")
        self.assertEqual(args.api_key, "api-key")
        self.assertEqual(script.get_api_key(args), "api-key")

    def test_args_env_variable(self):
        os.environ["EXABEL_API_KEY"] = "env_key"
        try:
            script = ExportSignals(self.common_args + ["foo.csv"], "desc")
            self.assertEqual(script.parser.description, "desc")
            args = script.parse_arguments()
            self._assert_common_args(args)
            self.assertIsNone(args.api_key)
            self.assertEqual(args.filename, "foo.csv")
            self.assertEqual(script.get_api_key(args), "env_key")
        finally:
            del os.environ["EXABEL_API_KEY"]

    def test_args_known_time(self):
        script = ExportSignals(
            self.common_args + ["foo.csv", "--api-key", "api-key", "--known-time", "2024-01-03"],
            "desc",
        )
        self.assertEqual(script.parser.description, "desc")
        args = script.parse_arguments()
        self._assert_common_args(args)
        self.assertEqual(args.known_time, pd.Timestamp("2024-01-03"))

    def test_args_missing_api_key(self):
        script = ExportSignals(self.common_args + ["foo.csv"], "desc")
        self.assertRaises(SystemExit, script.parse_arguments)

    def test_args_unknown_file_extension(self):
        script = ExportSignals(self.common_args + ["foo.pdf", "--api-key", "api-key"], "desc")
        self.assertRaises(SystemExit, script.parse_arguments)

    def test_args_unknown_date_format(self):
        script = ExportSignals(
            self.common_args + ["foo.pickle", "--api-key", "api-key", "--known-time", "Monday"],
            "desc",
        )
        self.assertRaises(SystemExit, script.parse_arguments)
