from exabel_data_sdk.client.api.api_client.grpc.model_grpc_client import ModelGrpcClient
from exabel_data_sdk.client.api.api_client.http.model_http_client import ModelHttpClient
from exabel_data_sdk.client.api.data_classes.model_run import ModelRun
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import CreateModelRunRequest


class ModelApi:
    """
    API class for model operations.
    """

    def __init__(self, config: ClientConfig, use_json: bool = False):
        self.client = (ModelHttpClient if use_json else ModelGrpcClient)(config)

    def create_model_run(self, run: ModelRun, model: str) -> ModelRun:
        """
        Create a model run.

        Args:
            run:    The model run to create.
            model:  The resource name of the model to create the run for.
                    Example: "models/123".
        """
        response = self.client.create_model_run(
            CreateModelRunRequest(run=run.to_proto(), parent=model)
        )
        return ModelRun.from_proto(response)
