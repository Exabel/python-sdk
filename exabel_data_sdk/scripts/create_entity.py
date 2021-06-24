import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateEntity(BaseScript):
    """
    Create an entity.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help=(
                "The resource name of the the new entity, "
                "for example 'entityTypes/brand/entities/brandIdentifier'"
            ),
        )
        self.parser.add_argument(
            "--display-name",
            required=True,
            type=str,
            help="The display name of the entity",
        )
        self.parser.add_argument(
            "--description",
            required=False,
            type=str,
            default="",
            help="One or more paragraphs of text description",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        name_parts = args.name.split("/")
        if len(name_parts) != 4:
            raise ValueError(f"Invalid resource name: {args.name}")
        entity_type = f"{name_parts[0]}/{name_parts[1]}"
        entity = Entity(
            name=args.name,
            display_name=args.display_name,
            description=args.description,
            properties={},
        )
        entity = client.entity_api.create_entity(entity=entity, entity_type=entity_type)
        print(entity)


if __name__ == "__main__":
    CreateEntity(sys.argv, "Create an entity.").run()
