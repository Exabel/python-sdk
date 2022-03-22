import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.derived_signal import (
    DerivedSignal,
    DerivedSignalMetaData,
    DerivedSignalUnit,
)
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateDerivedSignal(BaseScript):
    """
    Creates a new derived signal.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--label", required=True, type=str, help="The label of the signal."
        )
        self.parser.add_argument(
            "--expression", required=True, type=str, help="The signal expression."
        )
        self.parser.add_argument(
            "--description",
            required=False,
            type=str,
            default="",
            help="Description of the signal.",
        )
        self.parser.add_argument(
            "--unit",
            required=False,
            type=str,
            default="number",
            choices=["number", "ratio", "ratio_difference"],
            help="Unit of the derived signal. "
            'Valid values are "number", "ratio" and "ratio_difference".',
        )
        self.parser.add_argument(
            "--decimals",
            required=False,
            type=int,
            default=None,
            help="Number of decimals to use when displaying signal values.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        signal = client.derived_signal_api.create_derived_signal(
            DerivedSignal(
                name=None,
                label=args.label,
                expression=args.expression,
                description=args.description,
                metadata=DerivedSignalMetaData(
                    unit=self.get_unit(args.unit), decimals=args.decimals
                ),
            ),
        )
        print(f"Successfully created derived signal: {signal}")

    @staticmethod
    def get_unit(unit: str) -> DerivedSignalUnit:
        """Maps the given unit string into a DerivedSignalUnit."""
        if unit == "number":
            return DerivedSignalUnit.NUMBER
        if unit == "ratio":
            return DerivedSignalUnit.RATIO
        if unit == "ratio_difference":
            return DerivedSignalUnit.RATIO_DIFFERENCE

        raise ValueError(f"Unknown unit: {unit}")


if __name__ == "__main__":
    CreateDerivedSignal(sys.argv, "Create a new derived signal.").run()
