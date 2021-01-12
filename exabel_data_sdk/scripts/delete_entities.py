import argparse
import sys
from typing import List, Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.scripts.base_script import BaseScript


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

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        if args.dry_run:
            print("Running dry-run...")

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

        print(f"Total number of entities: {len(all_entities)}")
        entities_not_read_only = [entity for entity in all_entities if not entity.read_only]
        print(f"Number of not read-only entities: {len(entities_not_read_only)}")

        num_deleted = 0
        for entity in entities_not_read_only:
            if args.dry_run:
                print(f"Delete: {entity}")
            else:
                client.entity_api.delete_entity(entity.name)
                num_deleted += 1

        if args.dry_run:
            print(f"Would have deleted {num_deleted} entities")
        else:
            print(f"Successfully deleted {num_deleted} entities")


if __name__ == "__main__":
    DeleteEntities(sys.argv, "Deletes entities of a given type.").run()
