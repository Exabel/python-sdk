import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.prediction_model_run import PredictionModelRun
from exabel_data_sdk.scripts.base_script import BaseScript


class CreatePredictionModelRun(BaseScript):
    """
    Create a prediction model run.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--model",
            required=True,
            type=str,
            help="The resource name of the prediction model, for example 'predictionModels/123'.",
        )
        self.parser.add_argument(
            "--description",
            required=False,
            type=str,
            default="",
            help="Description of the run.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        model_run = client.prediction_model_api.create_run(
            model=args.model, run=PredictionModelRun(name="", description=args.description)
        )
        print(model_run)


if __name__ == "__main__":
    CreatePredictionModelRun(sys.argv, "Create a prediction model run.").run()
