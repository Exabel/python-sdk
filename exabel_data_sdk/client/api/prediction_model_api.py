from exabel_data_sdk.client.api.api_client.grpc.prediction_model_grpc_client import (
    PredictionModelGrpcClient,
)
from exabel_data_sdk.client.api.api_client.http.prediction_model_http_client import (
    PredictionModelHttpClient,
)
from exabel_data_sdk.client.api.data_classes.prediction_model_run import PredictionModelRun
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import CreatePredictionModelRunRequest


class PredictionModelApi:
    """
    API class for prediction model operations.
    """

    def __init__(self, config: ClientConfig, use_json: bool = False):
        self.client = (PredictionModelHttpClient if use_json else PredictionModelGrpcClient)(config)

    def create_run(self, run: PredictionModelRun, model: str) -> PredictionModelRun:
        """
        Create a prediction model run.

        Args:
            run:    The model run to create.
            model:  The resource name of the prediction model to create the run for.
                    Example: "predictionModels/123".
        """
        response = self.client.create_model_run(
            CreatePredictionModelRunRequest(run=run.to_proto(), parent=model)
        )
        return PredictionModelRun.from_proto(response)
