import argparse
import sys
from typing import List, Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.scripts.base_script import BaseScript


class ListEntities(BaseScript):
    """
    Lists all entities of a given entity type.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--entity-type",
            required=True,
            type=str,
            help="The entity type, for example 'entityTypes/ns.entityType'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        page_token = None
        all_entities: List[Entity] = []
        while True:
            result = client.entity_api.list_entities(
                entity_type=args.entity_type, page_size=1000, page_token=page_token
            )
            all_entities.extend(result.results)
            page_token = result.next_page_token
            if len(all_entities) == result.total_size:
                break

        if not all_entities:
            print("No entities of the given type.")

        for entity in all_entities:
            print(entity)


if __name__ == "__main__":
    ListEntities(sys.argv, "Lists entities of a given type.").run()
