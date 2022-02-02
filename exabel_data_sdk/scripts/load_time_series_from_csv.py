import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.csv_script_with_entity_mapping import CsvScriptWithEntityMapping
from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.csv_time_series_loader import CsvTimeSeriesLoader


class LoadTimeSeriesFromCsv(CsvScriptWithEntityMapping):
    """
    Processes a timeseries CSV file and uploads the time series to Exabel.

    The CSV file should have a header line on the format
        entityType;date;`signal_1`; ... ;`signal_n`

    For example
        brand;date;revenue;sales

    Each subsequent row consists of the following elements:
      * the entity referred to by the entity’s identifier
      * the date on ISO format, e.g. 2020-12-31
      * one numerical value for each of the signals `signal_1` to `signal_n`

    Thus, a typical row would look like:
        brand_1;2020-12-31;12;1234.56;1.23e6

    The rows do not have to be sorted in any particular order.
    """

    def __init__(self, argv: Sequence[str]):
        description = "Upload timeseries file."
        super().__init__(argv, description)
        self.parser.add_argument(
            "--create-missing-signals",
            required=False,
            action="store_true",
            default=False,
            help="Automatically create signals that are not already present in the API.",
        )
        self.parser.add_argument(
            "--pit-current-time",
            required=False,
            action="store_true",
            default=False,
            help=(
                "Set the Known-Time of the uploaded data to be "
                "the time at which it is inserted into the Exabel system."
            ),
        )
        self.parser.add_argument(
            "--pit-offset",
            required=False,
            type=int,
            choices=range(31),
            metavar="[0-30]",
            help=(
                "Set the Known-Time of the uploaded data to be the timestamp of each data point, "
                "plus the specified number of days as an offset. For instance, if the data is "
                "available to the user the day after, one would set --pit-offset 1"
            ),
        )
        self.parser.add_argument(
            "--no-create-library-signal",
            dest="create_library_signal",
            required=False,
            action="store_false",
            default=True,
            help="Set to not create library signal DSL expressions.",
        )
        self.parser.add_argument(
            "--no-create-tag",
            dest="create_tag",
            required=False,
            action="store_false",
            default=True,
            help="Set to not create a tag for every entity type a signal has time series for.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        try:
            CsvTimeSeriesLoader(client).load_time_series(
                filename=args.filename,
                entity_mapping_filename=args.entity_mapping_filename,
                separator=args.sep,
                namespace=args.namespace,
                pit_current_time=args.pit_current_time,
                pit_offset=args.pit_offset,
                create_missing_signals=args.create_missing_signals,
                create_tag=args.create_tag,
                create_library_signal=args.create_library_signal,
                threads=args.threads,
                dry_run=args.dry_run,
                retries=args.retries,
            )
        except CsvLoadingException as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    LoadTimeSeriesFromCsv(sys.argv).run()
