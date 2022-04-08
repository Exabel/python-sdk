import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class ShareFolder(BaseScript):
    """
    Share a folder with a group.
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
        self.parser.add_argument(
            "--write",
            required=False,
            action="store_true",
            help="Share with write access",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        client.library_api.share_folder(args.folder, args.group, write=args.write)
        print(
            f"Folder '{args.folder}' shared with group '{args.group}' "
            f"with {'write' if args.write else 'read only'} access."
        )


if __name__ == "__main__":
    ShareFolder(sys.argv, "Share a folder.").run()
