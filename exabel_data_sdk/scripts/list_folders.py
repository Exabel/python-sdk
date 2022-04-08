import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class ListFolders(BaseScript):
    """
    Lists all the accessible folders.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        folders = client.library_api.list_folders()
        print("Folders:")
        for folder in folders:
            print(f" {folder.name:<13} ({'w' if folder.write else 'r'}): {folder.display_name}")


if __name__ == "__main__":
    ListFolders(sys.argv, "List folders.").run()
