import argparse
import sys

from exabel import ExabelClient
from exabel.client.api.data_classes.relationship_type import RelationshipType
from exabel.scripts.base_script import BaseScript
from exabel.scripts.utils import PAGE_SIZE


class ListRelationshipTypes(BaseScript):
    """
    Lists relationship types.
    """

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        page_token = None
        all_relationship_types: list[RelationshipType] = []
        while True:
            result = client.relationship_api.list_relationship_types(
                page_size=PAGE_SIZE, page_token=page_token
            )
            all_relationship_types.extend(result.results)
            page_token = result.next_page_token
            if len(result.results) < PAGE_SIZE:
                break
        if not all_relationship_types:
            print("No relationship types.")
        for relationship_type in all_relationship_types:
            print(relationship_type)


if __name__ == "__main__":
    ListRelationshipTypes(sys.argv, "Lists relationship types.").run()
