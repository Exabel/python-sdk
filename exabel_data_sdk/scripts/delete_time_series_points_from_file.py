import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts import utils
from exabel_data_sdk.scripts.actions import CaseInsensitiveArgumentAction
from exabel_data_sdk.scripts.csv_script_with_entity_mapping import CsvScriptWithEntityMapping
from exabel_data_sdk.services.csv_loading_constants import DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.services.file_time_series_loader import FileTimeSeriesLoader


class DeleteTimeSeriesPointsFromFile(CsvScriptWithEntityMapping):
    """
    Processes a time series file and deletes the data points at given date and known_time values.

    CSV files can be processed, and there are two supported file layouts:
     * Signals as columns, with a header like: entityType, date, known_time, signal_1, ... ,signal_n
     * Signals as rows, with a header like: entityType, date, known_time, signal, value

    See the Exabel Help pages for a full documentation, and further examples.

    To delete data points on companies, set the entity header to one of: isin, factset_identifier,
    bloomberg_symbol, bloomberg_ticker, figi, mic:ticker or cusip, or use the identifier_type
    argument.
    Supported identifier types for security entities are isin, mic:ticker and cusip.

    To delete data points on generic entities, set it either to the entity type identifier,
    for example `brand`, or set it to the constant `entity`. If set to `entity` the entities must
    be identified by their full resource name, for example `entityTypes/brand/entities/b1`.

    Dates in CSV files should be on ISO format, e.g. 2020-12-31.

    The known_time column is required for deletion of data points.

    The rows do not have to be sorted in any particular order.
    """

    def __init__(self, argv: Sequence[str]):
        description = "Delete time series data points."
        super().__init__(argv, description)
        self.parser.add_argument(
            "--entity-type",
            type=utils.entity_type_resource_name,
            help=(
                "The entity type of the entities in the file. If not specified, the entity type "
                "will be inferred from the column name."
            ),
            action=CaseInsensitiveArgumentAction,
        )
        self.parser.add_argument(
            "--identifier-type",
            type=str,
            help="The identifier type used to map the entities in the file.",
            action=CaseInsensitiveArgumentAction,
        )
        self.parser.set_defaults(threads=DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT)
        self.parser.add_argument(
            "--batch-size",
            type=int,
            help=(
                "The number of rows in each batch to read and process from the file. If not "
                "specified, defaults to reading the entire file into memory before processing."
            ),
        )
        self.parser.add_argument(
            "--skip-validation",
            required=False,
            action="store_true",
            default=False,
            help="If set, the time series are not validated before uploading.",
        )
        self.parser.add_argument(
            "--case-sensitive-signals",
            required=False,
            action="store_true",
            default=False,
            help="If set, signal names are treated as case sensitive. Note that this will disable "
            "lowercasing of other column headers as well, as entities, 'date', and "
            "'known_time'. Take care to maintain correct casing in the file when using this "
            "option.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        try:
            FileTimeSeriesLoader(client).batch_delete_time_series_points(
                filename=args.filename,
                entity_mapping_filename=args.entity_mapping_filename,
                separator=args.sep,
                entity_type=args.entity_type,
                identifier_type=args.identifier_type,
                threads=args.threads,
                dry_run=args.dry_run,
                retries=args.retries,
                batch_size=args.batch_size,
                skip_validation=args.skip_validation,
                case_sensitive_signals=args.case_sensitive_signals,
                abort_threshold=args.abort_threshold,
            )
        except FileLoadingException as e:
            print("ERROR: Deleting time series data points failed.")
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    DeleteTimeSeriesPointsFromFile(sys.argv).run()
