import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateEntityType(BaseScript):
    """
    Create an entity type.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The resource name of the new entity type, for example 'entityTypes/ns.brand'",
        )
        self.parser.add_argument(
            "--display-name",
            required=True,
            type=str,
            help="The display name of the entity type",
        )
        self.parser.add_argument(
            "--description",
            required=False,
            type=str,
            default="",
            help="One or more paragraphs of text description",
        )
        is_associative_group = self.parser.add_mutually_exclusive_group(required=True)
        is_associative_group.add_argument(
            "--is-associative",
            default=None,
            required=False,
            action="store_true",
            help="Whether the entity type is associative",
        )
        is_associative_group.add_argument(
            "--no-is-associative",
            dest="is_associative",
            default=None,
            required=False,
            action="store_false",
            help="Whether the entity type is not associative",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        entity_type = EntityType(
            name=args.name,
            display_name=args.display_name,
            description=args.description,
            is_associative=args.is_associative,
        )
        entity = client.entity_api.create_entity_type(entity_type=entity_type)
        print(entity)


if __name__ == "__main__":
    CreateEntityType(sys.argv, "Create an entity type.").run()
