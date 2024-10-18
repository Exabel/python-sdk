import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.data_set import print_data_set
from exabel_data_sdk.scripts import utils
from exabel_data_sdk.scripts.base_script import BaseScript


class GetDataSet(BaseScript):
    """
    Gets a data set.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=utils.data_set_resource_name,
            help="The resource name of the data set, for example 'dataSets/ns.transactions'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        data_set = client.data_set_api.get_data_set(name=args.name)
        if data_set:
            print_data_set(data_set)
        else:
            print("Data set not found.")


if __name__ == "__main__":
    GetDataSet(sys.argv, "Get a data set.").run()
