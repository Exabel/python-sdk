import argparse
import sys
from typing import Sequence

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.client.api.data_classes.time_series import Dimension, TimeSeries, Unit, Units
from exabel_data_sdk.client.api.resource_creation_result import ResourceCreationStatus
from exabel_data_sdk.scripts import utils
from exabel_data_sdk.scripts.base_script import BaseScript


class UpsertTimeSeriesUnit(BaseScript):
    """
    Updates or creates a time series with the specified unit.
    """

    def __init__(self, argv: Sequence[str]):
        description = "Updates or creates a time series with a given unit."
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
            "--unit-type",
            required=False,
            type=str,
            default=None,
            help=(
                "The unit type of the time series. "
                "One of 'unknown', 'currency', 'mass', 'length', 'time', 'ratio'."
            ),
        )
        self.parser.add_argument(
            "--unit",
            required=False,
            type=str,
            default=None,
            help="The unit of the time series. For example 'USD' or 'EUR'.",
        )
        self.parser.add_argument(
            "--description",
            required=False,
            type=str,
            default=None,
            help="A description of the time series",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        units = Units(
            units=[Unit(dimension=Dimension.from_string(args.unit_type), unit=args.unit)],
            description=args.description,
        )
        series = [TimeSeries(series=pd.Series(data=[], name=args.name, dtype=object), units=units)]
        results = client.time_series_api.import_time_series(
            parent="signals/-", series=series, status_in_response=True
        )
        if results:
            for result in results:
                if result.status == ResourceCreationStatus.FAILED:
                    print("Failed to upsert time series.")
                    print(result.get_printable_error())
                    if isinstance(result.error, RequestError):
                        print(f"RequestError: {result.error.error_type.name}")
                else:
                    print("Upserted time series unit successfully")
                    print(result.resource)


if __name__ == "__main__":
    UpsertTimeSeriesUnit(sys.argv).run()
