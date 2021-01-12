import argparse
import sys
from typing import List

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.scripts.base_script import BaseScript


class ListSignals(BaseScript):
    """
    Lists all signals.
    """

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        page_token = None
        all_signals: List[Signal] = []
        while True:
            result = client.signal_api.list_signals(page_size=1000, page_token=page_token)
            all_signals.extend(result.results)
            page_token = result.next_page_token
            if len(all_signals) == result.total_size:
                break

        if not all_signals:
            print("No signals.")

        for signal in all_signals:
            print(signal)


if __name__ == "__main__":
    ListSignals(sys.argv, "Lists signals.").run()
