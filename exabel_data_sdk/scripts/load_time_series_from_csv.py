import argparse
import sys
from typing import List, Sequence

import pandas as pd
from dateutil import tz

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class LoadTimeSeriesFromCsv(BaseScript):
    """
    Processes a timeseries csv file and uploads to database
    The structure of the csv file will be on the format:
    entity;date;signal1; ... ;signalN

    Entity in the file will be Exabel entities
    Example: "entityTypes/company/entities/F_0027L0-E"

    Signals in the file will be defined signals
    Example: "signals/test.foursquare_signal"

    The rows do not have to be sorted
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
            type=lambda s: [str(item).strip() for item in s.split(",")],
            help="Delimited list input - separated with comma.",
        )
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of uploading.",
        )

    # get time series for an entity
    def get_time_series_for_entity(
        self, ts_data: pd.DataFrame, entity: str, signals: list
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

        if args.signals is None:
            ts_data = pd.read_csv(args.filename, header=0, sep=args.sep)
        else:
            ts_data = pd.read_csv(
                args.filename, header=0, sep=args.sep, names=["entity", "date"] + args.signals
            )

        # signals to produce from this csv file
        signals = ts_data.columns[2:]

        for entity in ts_data.entity.unique():
            time_series_list = self.get_time_series_for_entity(ts_data, entity, signals)

            # for each signal starting from column 2 -  upsert time series
            for time_series in time_series_list:

                if args.dry_run:
                    print(f"adding signal {time_series.name}")
                else:
                    client.time_series_api.upsert_time_series(time_series.name, time_series)


if __name__ == "__main__":
    LoadTimeSeriesFromCsv(sys.argv, "Upload timeseries file.").run()
