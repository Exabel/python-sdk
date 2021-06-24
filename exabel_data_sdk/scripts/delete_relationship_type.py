import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class DeleteRelationshipType(BaseScript):
    """
    Deletes a relationship type.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The resource name of the relationship type, "
            "for example 'relationshipTypes/ns.relationshipTypeIdentifier'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        client.relationship_api.delete_relationship_type(relationship_type=args.name)
        print("Successfully deleted the relationship type.")


if __name__ == "__main__":
    DeleteRelationshipType(sys.argv, "Delete a relationship type.").run()
