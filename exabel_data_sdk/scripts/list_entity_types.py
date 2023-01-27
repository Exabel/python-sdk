import argparse
import sys

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class ListEntityTypes(BaseScript):
    """
    Lists all entity types.
    """

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        all_entity_types = list(client.entity_api.get_entity_type_iterator())

        if not all_entity_types:
            print("No entity types.")

        for entity_type in all_entity_types:
            print(entity_type)


if __name__ == "__main__":
    ListEntityTypes(sys.argv, "Lists entity types.").run()
