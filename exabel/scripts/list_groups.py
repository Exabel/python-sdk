import argparse
import sys

from exabel import ExabelClient
from exabel.scripts.base_script import BaseScript


class ListGroups(BaseScript):
    """
    Lists all groups.
    """

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        groups = client.user_api.list_groups()
        for group in groups:
            print(group)


if __name__ == "__main__":
    ListGroups(sys.argv, "Lists groups.").run()
