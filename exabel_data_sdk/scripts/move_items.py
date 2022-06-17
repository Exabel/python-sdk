import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class MoveItems(BaseScript):
    """
    Move items to a folder
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--items",
            required=True,
            type=str,
            default=[],
            nargs="+",
            help="The resource names of the items to move",
        )
        self.parser.add_argument(
            "--to-folder",
            required=True,
            type=str,
            help="The resource name of the folder to move the items to",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        print("Moving items...")
        client.library_api.move_items(args.to_folder, args.items)
        folder = client.library_api.get_folder(args.to_folder)
        print(f"Folder '{folder.display_name}' now contains:")
        for item in folder.items:
            print(f" - {item.name}: {item.display_name}")


if __name__ == "__main__":
    MoveItems(sys.argv, "Move items to a folder.").run()
