import argparse
import sys
from typing import Sequence

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts import utils
from exabel_data_sdk.scripts.base_script import BaseScript


class DeleteTimeSeriesPoint(BaseScript):
    """
    Deletes a timeseries point at known-time.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=utils.time_series_resource_name,
            help="The resource name for the time series, for example "
            "'entityTypes/ns.EntityType/entities/ns.EntityName/signals/ns.signalIdentifier'",
        )
        self.parser.add_argument(
            "--date",
            required=True,
            type=str,
            help="The date value of the time series data point to delete.",
        )
        self.parser.add_argument(
            "--known-time",
            required=True,
            type=str,
            help="The point-in-time of the time series data point to delete.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        result = client.time_series_api.batch_delete_time_series_points(
            series=[
                pd.Series(
                    dtype="float64",
                    name=args.name,
                    index=[(pd.Timestamp(args.date), pd.Timestamp(args.known_time))],
                )
            ]
        )

        if result and not result.has_failure():
            print("Data point removed")


if __name__ == "__main__":
    DeleteTimeSeriesPoint(sys.argv, "Deletes a time series point at a given known time.").run()
