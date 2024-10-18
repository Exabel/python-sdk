import argparse
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Sequence

from tqdm import tqdm

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.scripts.list_entities import ListEntities
from exabel_data_sdk.scripts.utils import (
    ERROR,
    MAX_WORKERS,
    PAGE_SIZE,
    SUCCESS,
    conditional_progress_bar,
)


class DeleteEntities(ListEntities):
    """
    Deletes all entities of a given entity type.

    Only entities that are not read-only are deleted.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of deleting",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        print(f"Deleting entities of entity type: {args.entity_type}")
        all_entities = self._list_entities(
            client,
            entity_type=args.entity_type,
            limit=args.limit,
            show_progress=args.show_progress,
            exclude_read_only=True,
        )

        num_entities = len(all_entities)
        if not num_entities:
            return
        print(f"Number of entities to delete: {num_entities}")

        num_deleted = num_failed = 0

        def delete_entity(entity: Entity) -> int:
            try:
                client.entity_api.delete_entity(entity.name)
                return SUCCESS
            except RequestError as e:
                tqdm.write(f"Failed to delete: {entity.name} / {e.error_type}")
                return ERROR

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for i in conditional_progress_bar(
                range(0, num_entities, PAGE_SIZE),
                desc="Deleting entities: ",
                show_progress=args.show_progress,
            ):
                batch = (
                    all_entities[i : i + PAGE_SIZE]
                    if i + PAGE_SIZE < num_entities
                    else all_entities[i:]
                )

                if args.dry_run:
                    for entity in batch:
                        tqdm.write(f"Delete: {entity.name.split('/')[-1]}")
                    num_deleted += len(batch)
                    continue

                api_results = executor.map(delete_entity, batch)
                api_results_counter = Counter(api_results)
                num_deleted += api_results_counter[SUCCESS]
                num_failed += api_results_counter[ERROR]

        if args.dry_run:
            print(f"Would have deleted {num_deleted} entities")
            return
        print(f"Successfully deleted {num_deleted} entities")
        if num_failed > 0:
            print(f"Failed to delete {num_failed} entities")


if __name__ == "__main__":
    DeleteEntities(sys.argv, "Deletes entities of a given type.").run()
