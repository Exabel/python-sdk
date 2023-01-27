import argparse
import sys

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class ListSignals(BaseScript):
    """
    Lists all signals.
    """

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        all_signals = list(client.signal_api.get_signal_iterator())

        if not all_signals:
            print("No signals.")

        for signal in all_signals:
            print(signal)


if __name__ == "__main__":
    ListSignals(sys.argv, "Lists signals.").run()
