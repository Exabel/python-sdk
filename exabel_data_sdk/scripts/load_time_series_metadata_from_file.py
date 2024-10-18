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


class LoadTimeSeriesMetaDataFromFile(CsvScriptWithEntityMapping):
    """
    Processes a time series metadata file and uploads the data to Exabel.

    Both CSV and Excel files can be imported, and these are the supported file layouts:
     * Signals as rows, with a header like:
        `entityType`,signal,unit,dimension,description

    See the Exabel Help pages for a full documentation, and further examples.

    To import time series metadata on companies, set the entity header to one of: isin,
    factset_identifier, bloomberg_symbol, bloomberg_ticker, figi, mic:ticker or cusip, or use
    the identifier_type argument.
    Supported identifier types for security entities are isin, mic:ticker and cusip.

    To import data on generic entities, set it either to the entity type identifier, for example
    `brand`, or set it to the constant `entity`. If set to `entity` the entities must be identified
    by their full resource name, for example `entityTypes/brand/entities/b1`.

    The rows do not have to be sorted in any particular order.
    """

    def __init__(self, argv: Sequence[str]):
        description = "Upload file with metadata for time series."
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
        self.parser.add_argument(
            "--create-missing-signals",
            required=False,
            action="store_true",
            default=False,
            help="Automatically create signals that are not already present in the API.",
        )
        self.parser.add_argument(
            "--no-create-library-signal",
            dest="create_library_signal",
            required=False,
            action="store_false",
            default=True,
            help="Set to not create library signal DSL expressions.",
        )
        self.parser.set_defaults(threads=DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT)
        self.parser.add_argument(
            "--batch-size",
            type=int,
            help=(
                "The number of rows in each batch to read and upload from the file. If not "
                "specified, defaults to reading the entire file into memory before uploading."
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
            FileTimeSeriesLoader(client).load_time_series_metadata(
                filename=args.filename,
                entity_mapping_filename=args.entity_mapping_filename,
                separator=args.sep,
                entity_type=args.entity_type,
                identifier_type=args.identifier_type,
                create_missing_signals=args.create_missing_signals,
                create_library_signal=args.create_library_signal,
                threads=args.threads,
                dry_run=args.dry_run,
                retries=args.retries,
                abort_threshold=args.abort_threshold,
                batch_size=args.batch_size,
                skip_validation=args.skip_validation,
                case_sensitive_signals=args.case_sensitive_signals,
            )

        except FileLoadingException as e:
            print("ERROR: Loading time series failed.")
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    LoadTimeSeriesMetaDataFromFile(sys.argv).run()
