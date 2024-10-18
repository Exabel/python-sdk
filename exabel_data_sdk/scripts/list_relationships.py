import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.scripts import utils
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
            type=utils.relationship_type_resource_name,
            help=(
                "The resource name of the relationship type, "
                "for example 'relationshipTypes/ns.relationshipType'"
            ),
        )
        self.parser.add_argument(
            "--from-entity",
            required=False,
            type=utils.entity_resource_name,
            help="The resource name of the entity the relationships go from",
        )
        self.parser.add_argument(
            "--to-entity",
            required=False,
            type=utils.entity_resource_name,
            help="The resource name of the entity the relationships go to",
        )
        self.parser.add_argument(
            "--page-size",
            required=False,
            type=int,
            default=1000,
            help="The page size to use for retrieving all relationships"
            " (not applicable when specifying an entity)",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        if args.from_entity and args.to_entity:
            raise ValueError("Specify either the from entity or the to entity, not both.")
        entity = args.from_entity or args.to_entity
        if entity:
            # Check that the entity actually exists
            try:
                client.entity_api.get_entity(entity)
            except RequestError as error:
                print(error.message)
                return
        relationship_type = args.relationship_type
        if args.from_entity is not None:
            all_relationships = client.relationship_api.get_relationships_from_entity_iterator(
                relationship_type, entity
            )
        elif args.to_entity is not None:
            all_relationships = client.relationship_api.get_relationships_to_entity_iterator(
                relationship_type, entity
            )
        else:
            all_relationships = client.relationship_api.get_relationships_iterator(
                relationship_type, page_size=args.page_size
            )

        if not all_relationships:
            print("No relationships found")

        for relationship in all_relationships:
            print(relationship)


if __name__ == "__main__":
    ListRelationships(sys.argv, "Lists relationships of a given type.").run()
