import argparse
import re
import sys
from typing import List, Sequence

import pandas as pd
from dateutil import tz

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.scripts.csv_script import CsvScript
from exabel_data_sdk.util.resource_name_normalization import (
    to_entity_resource_names,
    validate_signal_name,
)


class LoadTimeSeriesFromCsv(CsvScript):
    """
    Processes a timeseries CSV file and uploads the time series to Exabel.

    The CSV file should have a header line on the format
        entity;date;`signal_1`; ... ;`signal_n`

    Each subsequent row consists of the following elements:
      * the entity referred to by the entity’s resource name, e.g.,
            entityTypes/company/entities/company_code
      * the date on ISO format, e.g. 2020-12-31
      * one numerical value for each of the signals `signal_1` to `signal_n`

    Thus, a typical row would look like:
        entityTypes/company/entities/company_code;2020-12-31;12;1234.56;1.23e6

    The rows do not have to be sorted in any particular order.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--create_missing_signals",
            required=False,
            action="store_true",
            default=False,
            help="Automatically create signals that are not already present in the API.",
        )

    def get_time_series(self, ts_data: pd.DataFrame, prefix: str) -> Sequence[pd.Series]:
        """Extract all the time series from the given data frame."""
        signals = ts_data.columns[2:]
        ts_data.index = pd.DatetimeIndex(ts_data.date, tz=tz.tzutc())
        ts_data.index.name = None
        series = []
        for entity, group in ts_data.groupby("entity"):
            for signal in signals:
                ts = group[signal].dropna()
                if ts.empty:
                    # Skip empty series
                    continue
                ts.name = f"{entity}/{prefix}{signal}"
                series.append(ts)
        return series

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        if args.dry_run:
            print("Running dry-run...")

        ts_data = self.read_csv(args, string_columns=[0])

        ts_data.iloc[:, 0] = to_entity_resource_names(
            client.entity_api, ts_data.iloc[:, 0], namespace=args.namespace
        )
        ts_data.rename(columns={0: "entity"}, inplace=True)
        if ts_data.columns[1] != "date":
            print("Expected first column to be named 'date', got", ts_data.columns[1])

        # signals to produce from this csv file
        signals = list(ts_data.columns[2:])

        print("Loading signals", ", ".join(str(s) for s in signals), "...")

        # validate signal names
        missing_header_pattern = re.compile(r"^Unnamed: ([0-9]+)$")
        missing_headers: List[str] = []
        invalid_signals: List[str] = []
        for signal in signals:
            try:
                validate_signal_name(signal)
            except ValueError:
                # Pandas eats up any blank column names and replaces them with "Unnamed: N". Since
                # this is invalid but not the actual column name, we give the end user a more
                # precise error message
                missing_header_match = missing_header_pattern.match(signal)
                if missing_header_match:
                    missing_headers.append(missing_header_match.group(1))
                else:
                    invalid_signals.append(signal)
        if invalid_signals or missing_headers:
            print(
                "Encountered invalid signal names. Signal names must start with a letter, "
                "and can only consist of letters, numbers, and underscore (_), and be "
                "at most 64 characters"
            )
            if invalid_signals:
                print(f"Invalid signal names: {', '.join(invalid_signals)}")
            if missing_headers:
                print(f"The following column(s) are missing headers: {', '.join(missing_headers)}")
            sys.exit(1)

        prefix = "signals/"
        if args.namespace:
            prefix += args.namespace + "."

        missing_signals = [
            signal for signal in signals if not client.signal_api.get_signal(prefix + signal)
        ]
        if missing_signals:
            print("Available signals are:")
            print(client.signal_api.list_signals())
            print("The following signals are missing:")
            print(missing_signals)
            if args.create_missing_signals and not args.dry_run:
                print("Creating the missing signals.")
                if not args.dry_run:
                    for signal in missing_signals:
                        client.signal_api.create_signal(
                            Signal(name=prefix + signal, display_name=signal),
                            create_library_signal=True,
                        )
            else:
                print("Aborting script. Please create the missing signals, and try again.")
                sys.exit(1)

        ts_data.columns = ["entity", "date"] + signals

        series = self.get_time_series(ts_data, prefix)

        if args.dry_run:
            print("Running the script would create the following time series:")
            for ts in series:
                print(f"    {ts.name}")
            return

        client.time_series_api.bulk_upsert_time_series(
            series, create_tag=True, threads=args.threads
        )


if __name__ == "__main__":
    LoadTimeSeriesFromCsv(sys.argv, "Upload timeseries file.").run()
