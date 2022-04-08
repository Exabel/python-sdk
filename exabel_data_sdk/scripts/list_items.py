import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.folder_item import FolderItemType
from exabel_data_sdk.scripts.base_script import BaseScript


class ListItems(BaseScript):
    """
    List items of a specific type.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--type",
            required=True,
            type=str,
            help="The item type",
        )
        self.parser.add_argument(
            "--folder-name",
            required=False,
            type=str,
            help="An optional folder resource name",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        item_type = FolderItemType[args.type]
        items = client.library_api.list_items(item_type, args.folder_name)
        print("Items:")
        for item in items:
            print(f" {item.name}:\t{item.display_name}")


if __name__ == "__main__":
    ListItems(sys.argv, "List items of a specific type.").run()
