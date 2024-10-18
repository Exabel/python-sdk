import argparse
import sys

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.data_set import print_data_set
from exabel_data_sdk.scripts.base_script import BaseScript


class ListDataSets(BaseScript):
    """
    Lists all data sets.
    """

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        all_data_sets = list(client.data_set_api.list_data_sets())

        if not all_data_sets:
            print("No data sets.")

        for data_set in all_data_sets:
            print_data_set(data_set)
            print()


if __name__ == "__main__":
    ListDataSets(sys.argv, "Lists data sets.").run()
