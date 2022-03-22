import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class DeleteEntityType(BaseScript):
    """
    Delete an entity type.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The resource name of the entity type, for example 'entityTypes/ns.brand'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        client.entity_api.delete_entity_type(name=args.name)
        print("Successfully deleted the entity type.")


if __name__ == "__main__":
    DeleteEntityType(sys.argv, "Delete an entity type.").run()
