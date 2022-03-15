import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.model_run import ModelRun
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateModelRun(BaseScript):
    """
    Create a model run.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--model",
            required=True,
            type=str,
            help="The resource name of the model, for example 'models/123'.",
        )
        self.parser.add_argument(
            "--description",
            required=False,
            type=str,
            default="",
            help="Description of the run.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        model_run = client.model_api.create_model_run(
            model=args.model, run=ModelRun(name="", description=args.description)
        )
        print(model_run)


if __name__ == "__main__":
    CreateModelRun(sys.argv, "Create a model run.").run()
