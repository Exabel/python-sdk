import argparse
import sys
from typing import Sequence

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.time_series import TimeSeries
from exabel_data_sdk.scripts import utils
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
            type=utils.time_series_resource_name,
            help=(
                "The resource name of a time series, for example "
                "'entityTypes/brand/entities/brandIdentifier/signals/ns.signalIdentifier'"
            ),
        )
        self.parser.add_argument(
            "--start",
            required=False,
            type=pd.Timestamp,
            help="The first date of the time series",
        )
        self.parser.add_argument(
            "--end",
            required=False,
            type=pd.Timestamp,
            help="The last date of the time series",
        )
        self.parser.add_argument(
            "--known-time",
            required=False,
            type=pd.Timestamp,
            help="The point-in-time to retrieve the time series at",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        result = client.time_series_api.get_time_series(
            args.name,
            start=args.start,
            end=args.end,
            known_time=args.known_time,
            include_metadata=True,
        )
        if result is None:
            print("Time series was not found")
            return

        assert isinstance(result, TimeSeries)
        if result.series.index.nlevels == 2:
            result.series.index = pd.MultiIndex.from_tuples(
                [(t.strftime("%Y-%m-%d"), k.strftime("%Y-%m-%d")) for t, k in result.series.index],
                names=["date", "known_time"],
            )
            if not args.known_time:
                result.series = result.series.droplevel("known_time")
        else:
            result.series.index = pd.Index(
                [t.strftime("%Y-%m-%d") for t in result.series.index], name="date"
            )

        pd.set_option("display.max_rows", None)
        pd.set_option(
            "display.float_format", "{:}".format  # pylint: disable=consider-using-f-string
        )
        print(result)


if __name__ == "__main__":
    GetTimeSeries(sys.argv).run()
