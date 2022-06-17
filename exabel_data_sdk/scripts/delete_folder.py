import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class DeleteFolder(BaseScript):
    """
    Delete an empty folder.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The resource name of the folder to delete, for example: 'folders/123'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        folder = client.library_api.get_folder(args.name)
        print(f"Deleting folder '{args.name}': '{folder.display_name}'...")
        client.library_api.delete_folder(args.name)
        print(f"Deleted folder '{args.name}'.")


if __name__ == "__main__":
    DeleteFolder(sys.argv, "Delete a folder.").run()
