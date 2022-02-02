import argparse
import os
from typing import Collection, Mapping, Optional, Sequence, Union

import pandas as pd

from exabel_data_sdk.scripts.base_script import BaseScript
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
)


class CsvScript(BaseScript):
    """
    Base class for scripts that process a CSV files with data to be loaded into the Exabel API.

    The first row of the CSV file should be a header row with column names.
    Each script will provide additional command line arguments that specify which columns to use.
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
            "--sep",
            required=False,
            type=str,
            default=",",
            help="Delimiter to use between cells.",
        )
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of uploading.",
        )
        namespace = os.getenv("EXABEL_NAMESPACE")
        help_text = "The customer's namespace into which to load the resources."
        if namespace:
            help_text += f" Defaults to '{namespace}' (from EXABEL_NAMESPACE environment variable)"
        else:
            help_text += " Can also be specified in the EXABEL_NAMESPACE environment variable."
        self.parser.add_argument(
            "--namespace",
            required=not namespace,
            type=str,
            default=namespace,
            help=help_text,
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

    def read_csv(
        self, args: argparse.Namespace, string_columns: Collection[Union[str, int]] = None
    ) -> pd.DataFrame:
        """Read the CSV file from disk with the filename specified by command line argument."""
        dtype: Optional[Mapping[Union[str, int], type]] = None
        if string_columns:
            dtype = {column: str for column in string_columns}
        return pd.read_csv(args.filename, header=0, sep=args.sep, dtype=dtype)
