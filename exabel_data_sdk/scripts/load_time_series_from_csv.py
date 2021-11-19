import argparse
import re
import sys
from typing import List, Sequence

import pandas as pd
from dateutil import tz
from google.protobuf.duration_pb2 import Duration
from pandas.api.types import is_numeric_dtype

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.scripts.csv_script_with_entity_mapping import CsvScriptWithEntityMapping
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import DefaultKnownTime
from exabel_data_sdk.util.resource_name_normalization import (
    to_entity_resource_names,
    validate_signal_name,
)


class LoadTimeSeriesFromCsv(CsvScriptWithEntityMapping):
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

    def __init__(self, argv: Sequence[str]):
        description = "Upload timeseries file."
        super().__init__(argv, description)
        self.parser.add_argument(
            "--create_missing_signals",
            required=False,
            action="store_true",
            default=False,
            help="Automatically create signals that are not already present in the API.",
        )
        self.parser.add_argument(
            "--pit_current_time",
            required=False,
            action="store_true",
            default=False,
            help="Set the Known-Time of the uploaded data to be "
            "the time at which it is inserted into the Exabel system.",
        )
        self.parser.add_argument(
            "--pit_offset",
            required=False,
            type=int,
            choices=range(31),
            metavar="[0-30]",
            help="Set the Known-Time of the uploaded data to be the timestamp of each data point, "
            "plus the specified number of days as an offset. For instance, if the data is "
            "available to the user the day after, one would set --pit_offset 1",
        )

    @staticmethod
    def set_time_index(ts_data: pd.DataFrame) -> None:
        """
        Creates a new index for the given data frame.
        There must be a 'date' column, which will be used as (the first level of) the new index.
        If there is a 'known_time' column, then the new index will be a MultiIndex with two levels,
        where the first level is 'date' and the second level is 'known_time'.
        If not, the new index will be a DatetimeIndex.
        The 'date' column is removed from the DataFrame, and so is the 'known_time' column,
        if present.
        """
        date_index = pd.DatetimeIndex(ts_data.date, tz=tz.tzutc())
        date_index.name = None
        if "known_time" in ts_data.columns:
            known_time_index = pd.DatetimeIndex(ts_data.known_time, tz=tz.tzutc())
            known_time_index.name = None
            ts_data.set_index([date_index, known_time_index], inplace=True)
            ts_data.drop(columns=["date", "known_time"], inplace=True)
        else:
            ts_data.set_index(date_index, inplace=True)
            ts_data.drop(columns="date", inplace=True)

    def get_time_series(self, ts_data: pd.DataFrame, prefix: str) -> Sequence[pd.Series]:
        """Extract all the time series from the given data frame."""
        signals = ts_data.columns[1:]
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

        default_known_time = None
        if args.pit_current_time:
            default_known_time = DefaultKnownTime(current_time=True)
        if args.pit_offset is not None:
            if default_known_time:
                print("Cannot specify both pit_current_time and pit_offset, it is one or the other")
                sys.exit(1)
            time_offset = Duration(seconds=86400 * args.pit_offset)
            default_known_time = DefaultKnownTime(time_offset=time_offset)

        ts_data = self.read_csv(args, string_columns=[0])
        entity_mapping = self.read_entity_mapping_file(args)
        if ts_data.columns[1] != "date":
            print("Expected second column to be named 'date', got", ts_data.columns[1])

        # signals to produce from this csv file
        signals = list(ts_data.columns[2:])

        if "known_time" in ts_data.columns:
            if args.pit_current_time:
                print(
                    "Specified pit_current_time on the command line, but file contains known_time"
                    " column.\nEither drop the pit_current_time command line argument, or"
                    " remove the known_time column from the file."
                )
                sys.exit(1)
            if args.pit_offset:
                print(
                    "Specified pit_offset on the command line, but file contains known_time"
                    " column.\nEither drop the pit_offset command line argument, or"
                    " remove the known_time column from the file."
                )
                sys.exit(1)
            # This column shall not be loaded as a signal
            signals.remove("known_time")
        else:
            if default_known_time is None:
                print("The Known-Time of the data must be specified.")
                print(
                    "Please add a column called known_time in the input file, or specify a "
                    "default policy with the pit_current_time or pit_offset command line "
                    "arguments."
                )
                sys.exit(1)

        ts_data.iloc[:, 0] = to_entity_resource_names(
            client.entity_api,
            ts_data.iloc[:, 0],
            namespace=args.namespace,
            entity_mapping=entity_mapping,
        )
        ts_data.rename(columns={ts_data.columns[0]: "entity"}, inplace=True)

        # validate all data points are numeric
        columns_with_invalid_data_points = {}
        for col in signals:
            if not is_numeric_dtype(ts_data[col]):
                examples = {
                    index: ts_data[col][index]
                    for index in ts_data[col][~ts_data[col].str.isnumeric()][:5].index
                }
                columns_with_invalid_data_points[col] = examples

        if columns_with_invalid_data_points:
            print(
                "Signal column(s) contain non-numeric values. Please ensure all values "
                "can be parsed to numeric values."
            )
            print("Columns with non-numeric values (with up to 5 examples):")
            for col, examples in columns_with_invalid_data_points.items():
                pretty_examples = ", ".join(
                    f"'{value}' at index {index}" for index, value in examples.items()
                )
                print(f"  {col}: {pretty_examples}")
            sys.exit(1)

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

        LoadTimeSeriesFromCsv.set_time_index(ts_data)
        series = self.get_time_series(ts_data, prefix)

        if args.dry_run:
            print("Running the script would create the following time series:")
            for ts in series:
                print(f"    {ts.name}")
            return

        try:
            client.time_series_api.bulk_upsert_time_series(
                series, create_tag=True, threads=args.threads, default_known_time=default_known_time
            )
        except BulkInsertFailedError:
            # An error summary has already been printed.
            pass


if __name__ == "__main__":
    LoadTimeSeriesFromCsv(sys.argv).run()
