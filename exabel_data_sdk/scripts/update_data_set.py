import argparse
import sys
from typing import List, Sequence

from google.protobuf.field_mask_pb2 import FieldMask

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.data_set import DataSet, print_data_set
from exabel_data_sdk.scripts import utils
from exabel_data_sdk.scripts.base_script import BaseScript


class UpdateDataSet(BaseScript):
    """
    Update a data set.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=utils.data_set_resource_name,
            help="The resource name of the data set, for example 'dataSets/ns.transactions'",
        )
        self.parser.add_argument(
            "--display-name",
            required=False,
            type=str,
            help="The display name of the data set",
        )
        self.parser.add_argument(
            "--description",
            required=False,
            type=str,
            help="One or more paragraphs of text description",
        )
        signals_group = self.parser.add_mutually_exclusive_group()
        signals_group.add_argument(
            "--signals",
            required=False,
            type=utils.signal_resource_name,
            nargs="+",
            help="Resource names of signals to set as or add to data set signals.",
        )
        signals_group.add_argument(
            "--signals-file",
            required=False,
            type=str,
            help="A plain text file to read signals from, with one signal resource name per line.",
        )
        signals_operation = self.parser.add_mutually_exclusive_group()
        signals_operation.add_argument(
            "--add-signals",
            required=False,
            action="store_true",
            help=(
                "Whether signals should be appended or replace the existing signals of the data "
                "set."
            ),
        )
        signals_operation.add_argument(
            "--remove-signals",
            required=False,
            action="store_true",
            help=(
                "Whether signals should be removed or replace the existing signals of the data "
                "set."
            ),
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        update_mask = []
        for field in ["display_name", "description"]:
            if getattr(args, field) is not None:
                update_mask.append(field)
        if args.signals or args.signals_file:
            update_mask.append("signals")
        if not update_mask:
            raise ValueError("No properties to update.")

        if args.add_signals and not args.signals and not args.signals_file:
            raise ValueError("Signals must be given when --add-signals is set.")

        signals: List[str] = []
        if args.signals:
            signals = args.signals
        elif args.signals_file:
            signals.extend(utils.read_signals_from_file(args.signals_file))

        if args.add_signals:
            existing_data_set = client.data_set_api.get_data_set(name=args.name)
            if existing_data_set is None:
                raise ValueError("Data set does not exist.")
            signals.extend(existing_data_set.signals)
        elif args.remove_signals:
            existing_data_set = client.data_set_api.get_data_set(name=args.name)
            if existing_data_set is None:
                raise ValueError("Data set does not exist.")
            signals = list(set(existing_data_set.signals).difference(set(signals)))

        data_set = DataSet(
            name=args.name,
            display_name=args.display_name if args.display_name is not None else "",
            description=args.description if args.description is not None else "",
            signals=list(set(signals)),
        )
        result = client.data_set_api.update_data_set(
            data_set=data_set, update_mask=FieldMask(paths=update_mask)
        )
        if result:
            print_data_set(result)


if __name__ == "__main__":
    UpdateDataSet(sys.argv, "Update a data set.").run()
