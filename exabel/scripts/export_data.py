import argparse
import sys
from typing import Sequence

from exabel import ExabelClient
from exabel.scripts.base_script import BaseScript


class ExportData(BaseScript):
    """Script for exporting data from the Exabel API with a user-provided query string."""

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.argv = argv
        self.parser.add_argument(
            "--query",
            required=True,
            type=str,
            help="The query to execute",
        )
        self.parser.add_argument(
            "--filename",
            required=True,
            type=str,
            help="The filename where the exported data should be saved",
        )
        self.parser.add_argument(
            "--format",
            required=True,
            type=str,
            help="The format",
        )
        self.parser.add_argument(
            "--retries",
            required=False,
            type=int,
            default=0,
            help="The maximum number of retries to make for each failed request. Defaults to 0.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        """Download data from the Exabel API and store it to file."""
        content = client.export_api.run_query_bytes(query=args.query, file_format=args.format)
        with open(args.filename, "wb") as file:
            file.write(content)


if __name__ == "__main__":
    ExportData(sys.argv, "Export data from Exabel").run()
