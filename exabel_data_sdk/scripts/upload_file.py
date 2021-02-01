import argparse
import sys
import pandas as pd
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript
from dateutil import tz


class UploadTimeseriesFile(BaseScript):
    """
    Processes a timeseries csv file and uploads
    Id's in the file will be Exabel entities
    The structure of the csv file will be on the format:
    entity, date, signal1 .. signalN
    The rows do not have to be sorted
    """
    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--filename",
            required=True,
            type=str,
            help="The name of the file to parse",
        )
        self.parser.add_argument(
            "--sep",
            required=False,
            type=str,
            default=';',
            help="Delimiter to use."
        )
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of uploading",
        )

    def run_script(self, client: ExabelClient,
        args: argparse.Namespace) -> None:
        if args.dry_run:
            print("Running dry-run...")

        ts_data = pd.read_csv(args.filename, header=0, sep=args.sep)

        # unique entities in the file
        unique_entities = ts_data.entity.unique()

        # signal values starts from column 2
        signals = ts_data.columns[2:]

        for entity in unique_entities:
            # collect all rows per entity
            entity_rows = ts_data.loc[ts_data.entity == entity]

            # get timeseries dates
            date_index = pd.DatetimeIndex(entity_rows.date, tz=tz.tzutc())

            # for each signal upsert time series
            for signal in signals:
                signal_values = entity_rows[signal].values
                time_series_name = f"{entity}/{signal}"

                if args.dry_run:
                    print(f"adding signal {time_series_name}")
                else:
                    client.time_series_api.upsert_time_series(
                      time_series_name,
                      pd.Series(
                        signal_values,
                        index=date_index
                      )
                    )


if __name__ == "__main__":
    UploadTimeseriesFile(sys.argv, "Upload timeseries file.").run()
