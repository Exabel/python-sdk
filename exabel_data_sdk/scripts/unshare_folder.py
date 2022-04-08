import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class UnshareFolder(BaseScript):
    """
    Unshare a folder with a group.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--folder",
            required=True,
            type=str,
            help="The resource name of the folder, for example 'folders/123'",
        )
        self.parser.add_argument(
            "--group",
            required=True,
            type=str,
            help="The resource name of the group, for example 'groups/987'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        client.library_api.unshare_folder(args.folder, args.group)
        print(f"Folder '{args.folder}' no longer shared with group '{args.group}'.")


if __name__ == "__main__":
    UnshareFolder(sys.argv, "Unshare a folder.").run()
