import argparse
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from math import ceil
from typing import Sequence

from tqdm import tqdm

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.scripts.base_script import BaseScript
from exabel_data_sdk.scripts.utils import (
    ERROR,
    MAX_WORKERS,
    PAGE_SIZE,
    SUCCESS,
    conditional_progress_bar,
)


class DeleteEntities(BaseScript):
    """
    Deletes all entities of a given entity type.

    Only entities that are not read-only are deleted.
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
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of deleting",
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

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        if args.dry_run:
            print("Running dry-run...")

        if not args.entity_type.startswith("entityTypes/"):
            args.entity_type = f"entityTypes/{args.entity_type}"

        print(f"Deleting entities of entity type: {args.entity_type}")
        print(f"Fetching entities in pages of size {PAGE_SIZE}...")
        page_token = None
        result = client.entity_api.list_entities(
            entity_type=args.entity_type, page_size=PAGE_SIZE, page_token=page_token
        )
        num_entities = result.total_size
        if not num_entities:
            print("No entities found")
            return

        print(f"Number of entities found: {num_entities}")
        if args.limit:
            print(f"Limiting to deleting {args.limit} entities")
            num_entities = min(num_entities, args.limit)

        num_read_only = 0
        all_entities = []
        for _ in conditional_progress_bar(
            range(1, ceil(num_entities / PAGE_SIZE) + 1),
            show_progress=args.show_progress,
            desc="Fetching entities: ",
            initial=1,
        ):
            entities_not_read_only = [
                entity.name for entity in result.results if not entity.read_only
            ]
            num_read_only += len(result.results) - len(entities_not_read_only)

            all_entities.extend(entities_not_read_only)

            page_token = result.next_page_token
            if page_token is None or len(all_entities) >= num_entities:
                break
            result = client.entity_api.list_entities(
                entity_type=args.entity_type, page_size=PAGE_SIZE, page_token=page_token
            )

        print(f"Number of read-only entities: {num_read_only}")
        if args.limit:
            all_entities = all_entities[: args.limit]
        num_entities = len(all_entities)
        if not num_entities:
            return
        print(f"Number of entities to delete: {num_entities}")

        num_deleted = num_failed = 0

        def delete_entity(entity_name: str) -> int:
            try:
                client.entity_api.delete_entity(entity_name)
                return SUCCESS
            except RequestError as e:
                tqdm.write(f"Failed to delete: {entity_name} / {e.error_type}")
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

                if not args.dry_run:
                    api_results = executor.map(delete_entity, batch)
                    api_results_counter = Counter(api_results)
                    num_deleted += api_results_counter[SUCCESS]
                    num_failed += api_results_counter[ERROR]
                else:
                    for entity in batch:
                        tqdm.write(f"Delete: {entity.split('/')[-1]}")
                    num_deleted += len(batch)

        if args.dry_run:
            print(f"Would have deleted {num_deleted} entities")
        else:
            print(f"Successfully deleted {num_deleted} entities")
            print(f"Failed to delete {num_failed} entities")


if __name__ == "__main__":
    DeleteEntities(sys.argv, "Deletes entities of a given type.").run()
