import argparse
import sys
from typing import List

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.scripts.base_script import BaseScript


class ListRelationshipTypes(BaseScript):
    """
    Lists relationship types.
    """

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        page_token = None
        all_relationship_types: List[RelationshipType] = []
        while True:
            result = client.relationship_api.list_relationship_types(
                page_size=1000, page_token=page_token
            )
            all_relationship_types.extend(result.results)
            page_token = result.next_page_token
            if len(all_relationship_types) == result.total_size:
                break
        if not all_relationship_types:
            print("No relationship types.")
        for relationship_type in all_relationship_types:
            print(relationship_type)


if __name__ == "__main__":
    ListRelationshipTypes(sys.argv, "Lists relationship types.").run()
