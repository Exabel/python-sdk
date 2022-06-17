import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.folder import Folder
from exabel_data_sdk.scripts.base_script import BaseScript


class UpdateFolder(BaseScript):
    """
    Update a folder with a new display name.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The resource name of the folder, for example 'folders/123'",
        )
        self.parser.add_argument(
            "--display-name",
            required=True,
            type=str,
            help="The new display name of the folder",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        folder = client.library_api.get_folder(args.name)
        print(f"Old folder name '{folder.name}': {folder.display_name}")
        new_folder = Folder(name=args.name, display_name=args.display_name, write=True, items=[])
        after_update = client.library_api.update_folder(new_folder)
        print(f"After update '{after_update.name}': {after_update.display_name}")


if __name__ == "__main__":
    UpdateFolder(sys.argv, "Update a folder.").run()
