import argparse
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest

from exabel.client.api.data_classes.derived_signal import DerivedSignal
from exabel.scripts.export_signals_v2 import ExportSignalsV2


class TestExportSignalsV2(unittest.TestCase):
    def setUp(self):
        self.common_args = [
            "script",
            "--signal",
            "signalA",
            "signalB",
            "--start-date",
            "2023-01-31",
            "--end-date",
            "2024-02-29",
            "--filename",
        ]

    def _assert_common_args(self, args: argparse.Namespace):
        assert args.signal == ["signalA", "signalB"]
        assert args.start_date == pd.Timestamp("2023-01-31")
        assert args.end_date == pd.Timestamp("2024-02-29")

    def test_args_with_tag(self):
        script = ExportSignalsV2(
            self.common_args
            + [
                "foo.csv",
                "--tag",
                "tags/user:1",
                "tags/user:2",
                "--api-key",
                "api-key",
            ],
            "desc",
        )
        args = script.parse_arguments()
        self._assert_common_args(args)
        assert args.filename == "foo.csv"
        assert args.tag == ["tags/user:1", "tags/user:2"]
        assert args.resource_name is None
        assert args.api_key == "api-key"

    def test_args_with_resource_name(self):
        script = ExportSignalsV2(
            self.common_args
            + [
                "foo.parquet",
                "--resource-name",
                "entityTypes/company/entities/A",
                "entityTypes/company/entities/B",
                "--api-key",
                "api-key",
            ],
            "desc",
        )
        args = script.parse_arguments()
        self._assert_common_args(args)
        assert args.filename == "foo.parquet"
        assert args.resource_name == [
            "entityTypes/company/entities/A",
            "entityTypes/company/entities/B",
        ]
        assert args.tag is None

    def test_args_env_variable(self):
        os.environ["EXABEL_API_KEY"] = "env_key"
        try:
            script = ExportSignalsV2(
                self.common_args
                + [
                    "foo.csv",
                    "--tag",
                    "tags/user:1",
                ],
                "desc",
            )
            args = script.parse_arguments()
            self._assert_common_args(args)
            assert args.api_key is None
            assert args.filename == "foo.csv"
        finally:
            del os.environ["EXABEL_API_KEY"]

    def test_args_known_time(self):
        script = ExportSignalsV2(
            self.common_args
            + [
                "foo.csv",
                "--tag",
                "tags/user:1",
                "--api-key",
                "api-key",
                "--known-time",
                "2024-01-03",
            ],
            "desc",
        )
        args = script.parse_arguments()
        assert args.known_time == pd.Timestamp("2024-01-03")

    def test_args_requires_entity_selector(self):
        script = ExportSignalsV2(self.common_args + ["foo.csv", "--api-key", "api-key"], "desc")
        with pytest.raises(SystemExit):
            script.parse_arguments()

    def test_args_tag_and_resource_name_mutually_exclusive(self):
        script = ExportSignalsV2(
            self.common_args
            + [
                "foo.csv",
                "--tag",
                "tags/user:1",
                "--resource-name",
                "entityTypes/company/entities/A",
                "--api-key",
                "api-key",
            ],
            "desc",
        )
        with pytest.raises(SystemExit):
            script.parse_arguments()

    def test_args_unknown_file_extension(self):
        script = ExportSignalsV2(
            self.common_args
            + [
                "foo.pdf",
                "--tag",
                "tags/user:1",
                "--api-key",
                "api-key",
            ],
            "desc",
        )
        with pytest.raises(SystemExit):
            script.parse_arguments()

    def test_args_expression_only(self):
        """--expression alone (no --signal) should parse and produce DerivedSignal objects."""
        script = ExportSignalsV2(
            [
                "script",
                "--expression",
                'brand_sales=data("sales").for_type("brand")',
                "--start-date",
                "2023-01-31",
                "--end-date",
                "2024-02-29",
                "--filename",
                "foo.csv",
                "--tag",
                "tags/user:1",
                "--api-key",
                "api-key",
            ],
            "desc",
        )
        args = script.parse_arguments()
        assert args.signal == []
        assert len(args.expression) == 1
        derived = args.expression[0]
        assert isinstance(derived, DerivedSignal)
        assert derived.label == "brand_sales"
        assert derived.expression == 'data("sales").for_type("brand")'

    def test_args_expression_without_equals_sign_raises(self):
        script = ExportSignalsV2(
            [
                "script",
                "--expression",
                "missing_separator",
                "--filename",
                "foo.csv",
                "--tag",
                "tags/user:1",
                "--api-key",
                "api-key",
            ],
            "desc",
        )
        with pytest.raises(SystemExit):
            script.parse_arguments()

    def test_args_expression_preserves_equals_in_expression_body(self):
        """`=` inside the expression must not confuse the label split."""
        script = ExportSignalsV2(
            [
                "script",
                "--expression",
                'cmp=data("x") == 1',
                "--filename",
                "foo.csv",
                "--tag",
                "tags/user:1",
                "--api-key",
                "api-key",
            ],
            "desc",
        )
        args = script.parse_arguments()
        derived = args.expression[0]
        assert derived.label == "cmp"
        assert derived.expression == 'data("x") == 1'

    def test_run_script_writes_raw_bytes_and_derives_format_from_extension(self):
        """`run_script` calls ``export_signals_v2_bytes`` with the format
        derived from the file extension and writes the returned bytes to
        disk verbatim (no pandas round-trip)."""
        with tempfile.TemporaryDirectory() as tmp:
            filename = str(Path(tmp) / "out.csv")
            wire_bytes = b"time,Sales\n2024-03-31,100\n"
            script = ExportSignalsV2(
                self.common_args
                + [
                    filename,
                    "--tag",
                    "tags/user:1",
                    "--api-key",
                    "api-key",
                ],
                "desc",
            )
            args = script.parse_arguments()

            client = MagicMock()
            client.export_api.export_signals_v2_bytes = MagicMock(return_value=wire_bytes)

            script.run_script(client, args)

            client.export_api.export_signals_v2_bytes.assert_called_once()
            kwargs = client.export_api.export_signals_v2_bytes.call_args.kwargs
            assert kwargs["file_format"] == "csv"
            assert kwargs["tag"] == ["tags/user:1"]
            assert kwargs["start_time"] == pd.Timestamp("2023-01-31")
            assert kwargs["end_time"] == pd.Timestamp("2024-02-29")
            assert Path(filename).read_bytes() == wire_bytes

    def test_run_script_derives_excel_format_from_xlsx_extension(self):
        """``.xlsx`` maps to ``file_format='excel'``, not the literal extension."""
        with tempfile.TemporaryDirectory() as tmp:
            filename = str(Path(tmp) / "out.xlsx")
            script = ExportSignalsV2(
                self.common_args
                + [
                    filename,
                    "--tag",
                    "tags/user:1",
                    "--api-key",
                    "api-key",
                ],
                "desc",
            )
            args = script.parse_arguments()

            client = MagicMock()
            client.export_api.export_signals_v2_bytes = MagicMock(return_value=b"PK\x03\x04")

            script.run_script(client, args)

            assert (
                client.export_api.export_signals_v2_bytes.call_args.kwargs["file_format"] == "excel"
            )
