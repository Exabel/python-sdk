import argparse
import sys
from typing import Sequence

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class GetTimeSeries(BaseScript):
    """
    Gets a time series.
    """

    def __init__(self, argv: Sequence[str]):
        description = "Gets a time series."
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help=(
                "The resource name of a time series, for example "
                "'entityTypes/brand/entities/brandIdentifier/signals/ns.signalIdentifier'"
            ),
        )
        self.parser.add_argument(
            "--start",
            required=False,
            type=str,
            help="The first date of the time series",
        )
        self.parser.add_argument(
            "--end",
            required=False,
            type=str,
            help="The last date of the time series",
        )
        self.parser.add_argument(
            "--known-time",
            required=False,
            type=str,
            help="The point-in-time to retrieve the time series at",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        start = pd.Timestamp(args.start) if args.start is not None else None
        end = pd.Timestamp(args.end) if args.end is not None else None
        known_time = pd.Timestamp(args.known_time) if args.known_time is not None else None
        result = client.time_series_api.get_time_series(
            args.name, start=start, end=end, known_time=known_time
        )
        print(result)


if __name__ == "__main__":
    GetTimeSeries(sys.argv).run()
