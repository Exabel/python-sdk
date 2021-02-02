import argparse
import sys
from typing import List, Sequence

import pandas as pd
from dateutil import tz

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class LoadTimeSeriesFromCsv(BaseScript):
    """
    Processes a timeseries CSV file and uploads the time series to Exabel.

    The CSV file should have a header line on the format
        entity;date;signals/`namespace`.`signal_1`; ... ;signals/`namespace`.`signal_n`
    where `namespace` is your namespace and `signal_1` to `signal_n` refer to signals you have
    created via the Exabel Data API.
    Alternatively you can pass a list of signal names with the --signals parameter to override the
    specified header names

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
            "--filename",
            required=True,
            type=str,
            help="The URL of the file to parse.",
        )
        self.parser.add_argument(
            "--sep", required=False, type=str, default=";", help="Delimiter to use between cells."
        )
        self.parser.add_argument(
            "--signals",
            required=False,
            nargs="+",
            type=str,
            help="Delimited list input - separated with comma.",
        )
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of uploading.",
        )

    def get_time_series_for_entity(
        self, ts_data: pd.DataFrame, entity: str, signals: List[str]
    ) -> List[pd.Series]:
        """
        Get a list of timeseries for an entity

        Args:
            ts_data:   Data frame on the format
                       ['entity', 'date', 'signal1', ..., 'signalN']
            entity:    The entity to create timeseries for
            signals:   List of signals to produce timeseries for
        """
        entity_rows = ts_data.loc[ts_data.entity == entity]

        time_series = []

        for signal in signals:
            series_values = self.get_time_series_for_signal(entity_rows, entity, signal)
            time_series.append(series_values)

        return time_series

    def get_time_series_for_signal(
        self, entity_rows: pd.DataFrame, entity: str, signal: str
    ) -> pd.Series:
        """
        Get a single timeseries for an entity

        Args:
            entity_rows:   Data frame on the format
                           ['entity', 'date', 'signal1', ..., 'signalN']
                           assumed to be filtered on the entity
            entity:        The name of the Entity this timeseries belongs to
            signal:        The signal to produce timeseries for
        """
        signal_values = entity_rows[signal].values
        date_index = pd.DatetimeIndex(entity_rows.date.values, tz=tz.tzutc())
        return pd.Series(signal_values, index=date_index, name=f"{entity}/{signal}")

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:

        if args.dry_run:
            print("Running dry-run...")

        if hasattr(args, "signals") and args.signals is not None:
            ts_data = pd.read_csv(
                args.filename, header=0, sep=args.sep, names=["entity", "date"] + args.signals
            )
        else:
            ts_data = pd.read_csv(args.filename, header=0, sep=args.sep)

        # signals to produce from this csv file
        signals = ts_data.columns[2:]

        for entity in ts_data.entity.unique():
            time_series_list = self.get_time_series_for_entity(ts_data, entity, signals)

            # for each signal starting from column 2 -  upsert time series
            for time_series in time_series_list:
                if args.dry_run:
                    print(f"adding timeseries for signal {time_series.name}")
                else:
                    client.time_series_api.upsert_time_series(time_series.name, time_series)


if __name__ == "__main__":
    LoadTimeSeriesFromCsv(sys.argv, "Upload timeseries file.")
