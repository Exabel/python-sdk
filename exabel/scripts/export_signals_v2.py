import argparse
import sys
from datetime import timedelta
from time import time
from typing import Sequence

import pandas as pd

from exabel import ExabelClient
from exabel.client.api.data_classes.derived_signal import DerivedSignal
from exabel.scripts.base_script import BaseScript

_EXTENSION_TO_FILE_FORMAT = {
    "csv": "csv",
    "xlsx": "excel",
    "json": "json",
    "feather": "feather",
    "parquet": "parquet",
}


def _validate_filename(filename: str) -> str:
    """Ensure the output file has one of the server-supported extensions."""
    extension = filename.rsplit(".", 1)[-1].lower()
    if extension not in _EXTENSION_TO_FILE_FORMAT:
        raise argparse.ArgumentTypeError(
            f"Unknown file extension {extension!r}. Supported: "
            + ", ".join(f".{e}" for e in _EXTENSION_TO_FILE_FORMAT)
        )
    return filename


def _parse_label_expression(value: str) -> DerivedSignal:
    """Parse a ``LABEL=EXPRESSION`` CLI value into a DerivedSignal.

    The label must be non-empty; the expression is everything after the first
    ``=`` so expressions containing ``=`` themselves (e.g. comparisons) still
    parse cleanly.
    """
    if "=" not in value:
        raise argparse.ArgumentTypeError(
            f"--expression value must be formatted as LABEL=EXPRESSION, got: {value!r}"
        )
    label, expression = value.split("=", 1)
    label = label.strip()
    expression = expression.strip()
    if not label or not expression:
        raise argparse.ArgumentTypeError(
            f"--expression value must have non-empty LABEL and EXPRESSION, got: {value!r}"
        )
    return DerivedSignal(name=None, label=label, expression=expression)


class ExportSignalsV2(BaseScript):
    """Export time series using the v2 signal export endpoint and write the raw
    server response to a file.

    Unlike ``export_signals``, this supports multi-time-series signals (e.g.
    signals whose expression uses ``for_type(...)`` and returns one series per
    sub-entity). Entities must be specified by resource name or tag;
    bloomberg_ticker / factset_id are not supported by the v2 endpoint.

    The output file contains the server's wire response verbatim (no pandas
    round-trip, no timezone normalization). Parquet and feather preserve the
    full multi-level column headers; csv, excel, and json are flattened per the
    server's serialization of those formats. Running this script does not
    require ``pyarrow`` — only the SDK and a network connection.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--signal",
            nargs="+",
            required=False,
            default=[],
            type=str,
            help=(
                "Signal label(s) to export from the library. "
                "At least one of --signal or --expression must be given."
            ),
        )
        self.parser.add_argument(
            "--expression",
            nargs="+",
            required=False,
            default=[],
            type=_parse_label_expression,
            help=(
                "DSL expression(s) to evaluate, each as LABEL=EXPRESSION. "
                "The LABEL becomes the column name in the output. Example: "
                "--expression "
                '\'brand_sales=data("sales").for_type("brand")\''
            ),
        )
        entity_group = self.parser.add_mutually_exclusive_group(required=True)
        entity_group.add_argument(
            "--resource-name",
            nargs="+",
            type=str,
            help="Entity resource name(s) to evaluate the signal(s) for.",
        )
        entity_group.add_argument(
            "--tag",
            nargs="+",
            type=str,
            help="Tag(s) whose entities should be evaluated.",
        )
        self.parser.add_argument(
            "--filename",
            required=True,
            type=_validate_filename,
            help=(
                "The filename to write the raw server response to. Supported extensions: "
                + ", ".join(f".{e}" for e in _EXTENSION_TO_FILE_FORMAT)
            ),
        )
        self.parser.add_argument(
            "--start-date",
            required=False,
            type=pd.Timestamp,
            help="The first date to evaluate the signals for.",
        )
        self.parser.add_argument(
            "--end-date",
            required=False,
            type=pd.Timestamp,
            help="The last date to evaluate the signals for.",
        )
        self.parser.add_argument(
            "--known-time",
            required=False,
            type=pd.Timestamp,
            help="The point-in-time at which to retrieve the time series.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        start_time = time()
        signals: list[str | DerivedSignal] = [*args.signal, *args.expression]
        if not signals:
            self.parser.error("at least one of --signal or --expression must be provided")
        signal_labels = [s if isinstance(s, str) else s.label for s in signals]
        print("Downloading signal(s):", ", ".join(signal_labels))

        extension = args.filename.rsplit(".", 1)[-1].lower()
        file_format = _EXTENSION_TO_FILE_FORMAT[extension]

        content = client.export_api.export_signals_v2_bytes(
            signals,
            file_format=file_format,
            resource_name=args.resource_name,
            tag=args.tag,
            start_time=args.start_date,
            end_time=args.end_date,
            version=args.known_time,
        )
        with open(args.filename, "wb") as f:
            f.write(content)

        spent_time = timedelta(seconds=int(time() - start_time))
        print(f"{len(content)} bytes written to {args.filename}, spent {spent_time}")


if __name__ == "__main__":
    ExportSignalsV2(
        sys.argv,
        "Export time series from the Exabel API for specified signals (v2 endpoint)",
    ).run()
