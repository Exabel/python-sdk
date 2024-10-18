import argparse
import sys
from typing import Sequence

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class ListSignals(BaseScript):
    """
    Lists all signals.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--only-name",
            required=False,
            action="store_true",
            help="Only output the signal names",
        )
        self.parser.add_argument(
            "--output-file",
            required=False,
            type=str,
            help="Export signals to CSV file",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        all_signals = list(client.signal_api.get_signal_iterator())

        if not all_signals:
            print("No signals.")

        if args.output_file:
            df = pd.DataFrame(all_signals).drop(columns=["entity_types", "read_only"])
            if args.only_name:
                df = df[["name"]]
            df.to_csv(args.output_file, index=False)
            print(f"Signals exported to {args.output_file}")
            return

        for signal in all_signals:
            if args.only_name:
                print(signal.name)
            else:
                print(signal)


if __name__ == "__main__":
    ListSignals(sys.argv, "Lists signals.").run()
