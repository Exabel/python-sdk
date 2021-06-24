import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.scripts.base_script import BaseScript


class GetRelationship(BaseScript):
    """
    Gets a relationship.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--relationship-type",
            required=True,
            type=str,
            help=(
                "The resource name of the relationship type, "
                "for example 'relationshipTypes/ns.relationshipType'"
            ),
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

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        try:
            client.entity_api.get_entity(args.from_entity)
            client.entity_api.get_entity(args.to_entity)
        except RequestError as error:
            print(error.message)
            return
        relationship = client.relationship_api.get_relationship(
            relationship_type=args.relationship_type,
            from_entity=args.from_entity,
            to_entity=args.to_entity,
        )
        print(relationship)


if __name__ == "__main__":
    GetRelationship(sys.argv, "Get a relationship.").run()
