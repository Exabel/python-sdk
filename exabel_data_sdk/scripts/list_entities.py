import argparse
import sys
from math import ceil
from typing import List, Optional, Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.scripts import utils
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
            type=utils.entity_type_resource_name,
            help="The entity type, for example 'entityTypes/ns.entityType'",
        )
        self.parser.add_argument(
            "--show-progress",
            required=False,
            action="store_true",
            default=False,
            help="Show progress bar",
        )
        self.parser.add_argument(
            "--limit",
            required=False,
            type=int,
            help="The maximum number of entities to delete",
        )

    @staticmethod
    def _filter_list(
        entity_list: Sequence[Entity], exclude_read_only: bool = False
    ) -> Sequence[Entity]:
        if exclude_read_only:
            return [e for e in entity_list if not e.read_only]
        return entity_list

    def _list_entities(
        self,
        client: ExabelClient,
        entity_type: str,
        limit: Optional[int] = None,
        show_progress: bool = False,
        exclude_read_only: bool = False,
    ) -> Sequence[Entity]:
        result = client.entity_api.list_entities(entity_type=entity_type, page_size=PAGE_SIZE)
        num_entities = result.total_size
        if not num_entities:
            print("No entities found")
            return []

        print(f"Number of entities found: {num_entities}")
        if limit:
            print(f"Limiting to {limit} entities")
            num_entities = min(num_entities, limit)

        all_entities: List[Entity] = []
        for _ in conditional_progress_bar(
            range(1, ceil(num_entities / PAGE_SIZE) + 1),
            show_progress=show_progress,
            desc="Fetching entities: ",
            initial=1,
        ):
            all_entities.extend(self._filter_list(result.results, exclude_read_only))

            if len(result.results) < PAGE_SIZE:
                break
            result = client.entity_api.list_entities(
                entity_type=entity_type, page_size=PAGE_SIZE, page_token=result.next_page_token
            )

        if limit:
            all_entities = all_entities[:limit]
        return all_entities

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        all_entities = self._list_entities(client, args.entity_type, args.limit, args.show_progress)

        for entity in all_entities:
            print(entity)


if __name__ == "__main__":
    ListEntities(sys.argv, "Lists entities of a given type.").run()
