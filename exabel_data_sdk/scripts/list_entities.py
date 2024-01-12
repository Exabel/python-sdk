import argparse
import sys
from math import ceil
from typing import List, Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.scripts.base_script import BaseScript
from exabel_data_sdk.scripts.utils import PAGE_SIZE, conditional_progress_bar


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
        self.parser.add_argument(
            "--show-progress",
            required=False,
            action="store_true",
            default=False,
            help="Show progress bar",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        if not args.entity_type.startswith("entityTypes/"):
            args.entity_type = f"entityTypes/{args.entity_type}"

        page_token = None
        all_entities: List[Entity] = []
        result = client.entity_api.list_entities(
            entity_type=args.entity_type, page_size=PAGE_SIZE, page_token=page_token
        )
        num_entities = result.total_size
        print(f"Number of entities found: {num_entities}")
        for _ in conditional_progress_bar(
            range(1, ceil(num_entities / PAGE_SIZE) + 1),
            show_progress=args.show_progress,
            desc="Fetching entities: ",
            initial=1,
        ):
            all_entities.extend(result.results)
            page_token = result.next_page_token
            if page_token is None or len(all_entities) >= num_entities:
                break
            result = client.entity_api.list_entities(
                entity_type=args.entity_type, page_size=PAGE_SIZE, page_token=page_token
            )

        for entity in all_entities:
            print(entity)


if __name__ == "__main__":
    ListEntities(sys.argv, "Lists entities of a given type.").run()
