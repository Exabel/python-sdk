import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class ListFolderAccessors(BaseScript):
    """
    List folder accessors
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The folder resource name, for example: 'folders/123'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        accessors = client.library_api.list_folder_accessors(args.name)
        print(f"Folder accessors for {args.name}:")
        for accessor in accessors:
            print(
                f" {accessor.group.name:<10} ({'w' if accessor.write else 'r'}): "
                f"{accessor.group.display_name}"
            )


if __name__ == "__main__":
    ListFolderAccessors(sys.argv, "List accessors of a folder.").run()
