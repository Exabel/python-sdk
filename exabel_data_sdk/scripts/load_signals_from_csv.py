import argparse
import sys
from typing import Sequence

import pandas as pd
from google.protobuf.field_mask_pb2 import FieldMask

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.scripts.base_script import BaseScript


class LoadSignalsFromCsv(BaseScript):
    """
    Processes a CSV file with signals and upserts them to Exabel.

    The header needs to have at least the columns 'name' and 'display_name'.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--filename",
            required=True,
            type=str,
            help="The URL of the file to parse.",
        )
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of uploading.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        signals = pd.read_csv(args.filename)
        signals.columns = signals.columns.str.lower()
        columns = ["name", "display_name"]
        if "description" in signals.columns:
            columns.append("description")
        try:
            signals = signals[columns]
        except KeyError:
            print("CSV file needs to at least have columns: name, display_name")
            return

        print(signals)
        if input(f"Do you want to create or update {len(signals)} signals? [Y/n]").upper() != "Y":
            print("Aborting.")
            return

        for _, row in signals.iterrows():
            description = row.get("description")
            if pd.isna(description):
                description = ""
            signal = Signal(
                name=row["name"],
                display_name=row.get("display_name"),
                description=description,
            )
            if not args.dry_run:
                paths = ["display_name"]
                if signal.description:
                    paths.append("description")
                signal = client.signal_api.update_signal(
                    signal=signal,
                    update_mask=FieldMask(paths=paths),
                    allow_missing=True,
                )
            print(signal)


if __name__ == "__main__":
    LoadSignalsFromCsv(sys.argv, "Load signals from csv.").run()
