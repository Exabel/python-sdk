import argparse
import sys

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class ListUsers(BaseScript):
    """
    Lists all users.
    """

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        users = client.user_api.list_users()
        for user in users:
            print(user)


if __name__ == "__main__":
    ListUsers(sys.argv, "Lists users.").run()
