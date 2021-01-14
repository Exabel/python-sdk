import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateRelationshipType(BaseScript):
    """
    Creates a new relationship type.
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
        self.parser.add_argument(
            "--description",
            required=True,
            type=str,
            help="One or more paragraphs of text description",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        relationship_type = client.relationship_api.create_relationship_type(
            RelationshipType(name=args.name, description=args.description, properties={})
        )
        print("Successfully created relationship type:")
        print(relationship_type)


if __name__ == "__main__":
    CreateRelationshipType(sys.argv, "Create a new relationship type.").run()
