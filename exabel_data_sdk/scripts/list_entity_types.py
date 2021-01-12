import argparse
import sys
from typing import List

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.scripts.base_script import BaseScript


class ListEntityTypes(BaseScript):
    """
    Lists all entity types.
    """

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        page_token = None
        all_entity_types: List[EntityType] = []
        while True:
            result = client.entity_api.list_entity_types(page_size=1000, page_token=page_token)
            all_entity_types.extend(result.results)
            page_token = result.next_page_token
            if len(all_entity_types) == result.total_size:
                break

        if not all_entity_types:
            print("No entity types.")

        for entity_type in all_entity_types:
            print(entity_type)


if __name__ == "__main__":
    ListEntityTypes(sys.argv, "Lists entity types.").run()
