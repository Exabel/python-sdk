import argparse
import sys
from typing import List, Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.scripts.base_script import BaseScript


class ListRelationships(BaseScript):
    """
    Lists all entities of a given entity type.
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
            required=False,
            type=str,
            help="The resource name of the entity the relationships go from",
        )
        self.parser.add_argument(
            "--to-entity",
            required=False,
            type=str,
            help="The resource name of the entity the relationships go to",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        if (args.from_entity is None) == (args.to_entity is None):
            raise ValueError("Specify either the from entity or the to entity.")
        entity = args.from_entity or args.to_entity
        try:
            client.entity_api.get_entity(entity)
        except RequestError as error:
            print(error.message)
            return
        page_token = None
        all_relationships: List[Relationship] = []
        while True:
            if args.from_entity is not None:
                result = client.relationship_api.get_relationships_from_entity(
                    relationship_type=args.relationship_type,
                    from_entity=args.from_entity,
                    page_size=1000,
                    page_token=page_token,
                )
            else:
                result = client.relationship_api.get_relationships_to_entity(
                    relationship_type=args.relationship_type,
                    to_entity=args.to_entity,
                    page_size=1000,
                    page_token=page_token,
                )
            all_relationships.extend(result.results)
            page_token = result.next_page_token
            if len(all_relationships) == result.total_size:
                break

        if not all_relationships:
            print("No relationships of the given type.")

        for relationship in all_relationships:
            print(relationship)


if __name__ == "__main__":
    ListRelationships(sys.argv, "Lists relationships of a given type.").run()
