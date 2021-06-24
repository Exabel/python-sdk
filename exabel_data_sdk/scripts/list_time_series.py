import argparse
import sys
from typing import List, Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class ListTimeSeries(BaseScript):
    """
    Lists all time series.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--signal",
            required=False,
            type=str,
            help="The resource name of a signal, for example 'signals/ns.signalIdentifier'",
        )
        self.parser.add_argument(
            "--entity",
            required=False,
            type=str,
            help=(
                "The resource name of an entity, "
                "for example 'entityTypes/company/entities/identifier'"
            ),
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        if (args.signal is None) == (args.entity is None):
            raise ValueError("Specify either signal or entity, but not both.")
        page_token = None
        all_time_series: List[str] = []
        while True:
            if args.signal is not None:
                result = client.time_series_api.get_signal_time_series(
                    args.signal, page_size=1000, page_token=page_token
                )
            else:
                result = client.time_series_api.get_entity_time_series(
                    args.entity, page_size=1000, page_token=page_token
                )
            all_time_series.extend(result.results)
            page_token = result.next_page_token
            if len(all_time_series) == result.total_size:
                break

        if not all_time_series:
            print("No time series.")

        for time_series in all_time_series:
            print(time_series)


if __name__ == "__main__":
    ListTimeSeries(sys.argv, "Lists time series.").run()
