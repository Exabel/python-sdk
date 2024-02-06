import argparse
import logging
import os
import sys
from datetime import timedelta
from time import time
from typing import List, Sequence, Set

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.export_api import ExportApi
from exabel_data_sdk.scripts.base_script import BaseScript
from exabel_data_sdk.scripts.file_utils import (
    supported_formats_message,
    to_file,
    validate_file_extension,
)


class ExportSignals(BaseScript):
    """Script for exporting time series from the Exabel API for specified signals."""

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--signal",
            nargs="+",
            required=True,
            type=str,
            help="The signal(s) to export",
        )
        self.parser.add_argument(
            "--tag",
            nargs="+",
            required=True,
            type=str,
            help="The tag(s) with entities for which to evaluate the signal(s)",
        )
        self.parser.add_argument(
            "--filename",
            required=True,
            type=validate_file_extension,
            help=(
                "The filename where the exported data should be saved. "
                + supported_formats_message()
            ),
        )
        self.parser.add_argument(
            "--start-date",
            required=False,
            type=pd.Timestamp,
            help="The first date to evaluate the signals for",
        )
        self.parser.add_argument(
            "--end-date",
            required=False,
            type=pd.Timestamp,
            help="The last date to evaluate the signals for",
        )
        self.parser.add_argument(
            "--known-time",
            required=False,
            type=pd.Timestamp,
            help="The point-in-time to retrieve the time series at",
        )
        self.parser.add_argument(
            "--batch-size",
            type=int,
            help="The number of entities to evaluate in each batch.",
            default=100,
        )
        self.parser.add_argument(
            "--retries",
            type=int,
            help="The number of times to retry each request.",
            default=3,
        )
        self.parser.add_argument(
            "--show-progress",
            required=False,
            action="store_true",
            default=False,
            help="Show progress bar",
        )

    @staticmethod
    def get_api_key(args: argparse.Namespace) -> str:
        """
        Get the API key to use, either from the command line arguments or the environment.
        Raises SystemExit if there is no API key provided.
        """
        api_key = args.api_key or os.getenv("EXABEL_API_KEY")
        if not api_key:
            print("No API key specified.")
            print("Use the --api-key command line argument or EXABEL_API_KEY environment variable.")
            sys.exit(1)
        return api_key

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        """Download data from the Exabel API and store it to file."""
        api_key = self.get_api_key(args)
        start_time = time()
        tag_results: List[Set[str]] = []
        for tag in args.tag:
            if not tag.startswith("tags/"):
                tag = f"tags/{tag}"
            result = set(client.tag_api.get_entity_iterator(tag))
            tag_results.append(result)
            print("Found", len(result), "entities in tag", tag)
        entities = tag_results[0]
        if len(tag_results) > 1:
            entities = entities.union(*tag_results[1:])
            print("In total", len(entities), "entities")
        export_api = ExportApi.from_api_key(api_key, retries=args.retries)
        signals = args.signal
        print("Downloading signal(s):", ", ".join(signals))
        logging.getLogger("exabel_data_sdk.client.api.export_api").setLevel(logging.WARNING)
        data = export_api.batched_signal_query(
            batch_size=args.batch_size,
            signal=signals,
            resource_name=list(entities),
            start_time=args.start_date,
            end_time=args.end_date,
            version=args.known_time,
            show_progress=args.show_progress,
        )
        if isinstance(data, pd.Series):
            data = data.to_frame()
        # Remove timezone information (all dates are UTC, and Excel doesn't support timezone)
        data.index = pd.MultiIndex.from_arrays(
            [data.index.get_level_values(0), data.index.get_level_values(1).tz_localize(None)],
            names=data.index.names,
        )
        to_file(data, args.filename)
        spent_time = timedelta(seconds=int(time() - start_time))
        print(f"{data.shape[0]} rows of data written to {args.filename}, spent {spent_time}")


if __name__ == "__main__":
    ExportSignals(sys.argv, "Export time series from the Exabel API for specified signals").run()
