import argparse
import sys
from typing import Sequence

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.list_time_series import ListTimeSeries
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
)


class DeleteTimeSeriesPoints(ListTimeSeries):
    """
    Deletes all time series data points for a specifc date and known time.
    The script fetches all time series for a given signal, entity type or
    entity, or a combination of these.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--date",
            required=True,
            type=str,
            help="The date of the time series point to delete.",
        )
        self.parser.add_argument(
            "--known-time",
            required=False,
            type=str,
            help="The known time of the time series point to delete.",
        )
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of deleting",
        )
        self.parser.add_argument(
            "--threads",
            required=False,
            type=int,
            choices=range(1, 101),
            metavar="[1-100]",
            default=DEFAULT_NUMBER_OF_THREADS,
            help=f"The number of parallel upload threads to run. "
            f"Defaults to {DEFAULT_NUMBER_OF_THREADS}.",
        )
        self.parser.add_argument(
            "--retries",
            required=False,
            type=int,
            choices=range(1, 51),
            metavar="[1-50]",
            default=DEFAULT_NUMBER_OF_RETRIES,
            help=f"The maximum number of retries to make for each failed request. Defaults to "
            f"{DEFAULT_NUMBER_OF_RETRIES}.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        all_time_series = self._list_time_series(
            client,
            entity=args.entity,
            signal=args.signal,
            entity_type=args.entity_type,
            show_progress=args.show_progress,
        )

        if not all_time_series:
            print("Did not find any time series.")
            return

        num_time_series = len(all_time_series)
        print(f"Number of time series data points to delete: {num_time_series}")

        date = pd.Timestamp(args.date)
        known_time = pd.Timestamp(args.known_time) if args.known_time else None

        index = (
            pd.MultiIndex.from_tuples([(date, known_time)], names=["date", "known_time"])
            if known_time
            else pd.Index([date], name="date")
        )

        series = [pd.Series([1], index=index, name=time_series) for time_series in all_time_series]

        print(f"Deleting time series data points with date {args.date}", end=" ")
        if known_time:
            print(f"and known time {args.known_time}", end=" ")
        print(f"from the following {num_time_series} time series.")

        for ts in series:
            print(ts.name)

        if args.dry_run:
            print(f"Would have deleted {num_time_series} time series data points.")
            return

        result = client.time_series_api.batch_delete_time_series_points(
            series, args.threads, args.retries
        )

        print(f"Successfully deleted {result.total_count} time series data points.")
        if result.has_failure():
            print(f"Failed to delete {len(result.get_failures())} time series data points.")


if __name__ == "__main__":
    DeleteTimeSeriesPoints(
        sys.argv,
        "Deletes all time series data points for a given date and known time. "
        "A signal, entity type, or entity, or a combination of these, can be specified "
        "to filter the time series to delete.",
    ).run()
