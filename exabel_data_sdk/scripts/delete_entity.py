import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript

class DeleteEntity(BaseScript):
    """
    Deletes one entity unless it is read-only.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--entity-id",
            required=True,
            type=str,
            help="The entity id, for example 'EXAMPLE_ID'",
        )
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of deleting",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        if args.dry_run:
            print("Running dry-run...")



if __name__ == "__main__";
    DeleteEntity(sys.argv, "Delete one entity with a given id.").run()
