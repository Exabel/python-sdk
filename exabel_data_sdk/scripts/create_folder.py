import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.folder import Folder
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateFolder(BaseScript):
    """
    Create a new folder.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--display-name",
            required=True,
            type=str,
            help="The display name of the new folder",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        new_folder = Folder(name="", display_name=args.display_name, write=True, items=[])
        folder = client.library_api.create_folder(new_folder)
        print(f"Created folder '{folder.name}': {folder.display_name}")


if __name__ == "__main__":
    CreateFolder(sys.argv, "Create a new folder.").run()
