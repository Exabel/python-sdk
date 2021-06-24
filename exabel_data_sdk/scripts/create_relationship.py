import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateRelationship(BaseScript):
    """
    Creates a new relationship.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--relationship-type",
            required=True,
            type=str,
            help="The resource name of the relationship type, "
            "for example 'relationshipTypes/ns.relationshipTypeIdentifier'",
        )
        self.parser.add_argument(
            "--from-entity",
            required=True,
            type=str,
            help="The resource name of the entity the relationship goes from",
        )
        self.parser.add_argument(
            "--to-entity",
            required=True,
            type=str,
            help="The resource name of the entity the relationship goes to",
        )
        self.parser.add_argument(
            "--description",
            required=True,
            type=str,
            help="One or more paragraphs of text description",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        relationship = client.relationship_api.create_relationship(
            Relationship(
                relationship_type=args.relationship_type,
                from_entity=args.from_entity,
                to_entity=args.to_entity,
                description=args.description,
                properties={},
            )
        )
        print("Successfully created relationship:")
        print(relationship)


if __name__ == "__main__":
    CreateRelationship(sys.argv, "Create a new relationship.").run()
