import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class GetFolder(BaseScript):
    """
    Get a folder.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The resource name of the folder, for example 'folders/123'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        folder = client.library_api.get_folder(args.name)
        print(f"Folder '{folder.name}': {folder.display_name}")
        print(f"Write access: {folder.write}")
        for item in folder.items:
            print(f" {item.name}:\t{item.display_name}")


if __name__ == "__main__":
    GetFolder(sys.argv, "Get a folder.").run()
