from typing import Iterator, Sequence

from google.protobuf.field_mask_pb2 import FieldMask

from exabel.client.api.api_client.grpc.prediction_model_grpc_client import (
    PredictionModelGrpcClient,
)
from exabel.client.api.data_classes.paging_result import PagingResult
from exabel.client.api.data_classes.prediction_model import PredictionModel
from exabel.client.api.data_classes.prediction_model_run import PredictionModelRun
from exabel.client.api.data_classes.request_error import ErrorType, RequestError
from exabel.client.client_config import ClientConfig
from exabel.stubs.exabel.api.analytics.v1.prediction_model_service_pb2 import (
    CreatePredictionModelRequest,
    CreatePredictionModelRunRequest,
    GetPredictionModelRequest,
    GetPredictionModelRunRequest,
    ListPredictionModelRunsRequest,
    ListPredictionModelsRequest,
    UpdatePredictionModelRequest,
)


class PredictionModelApi:
    """
    API class for prediction model operations.
    """

    def __init__(self, config: ClientConfig):
        self.client = PredictionModelGrpcClient(config)

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

    def get_model(self, name: str) -> PredictionModel | None:
        """Inspect a model, returning None only when it does not exist."""
        try:
            response = self.client.get_model(GetPredictionModelRequest(name=name))
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise
        return PredictionModel.from_proto(response)

    def list_models(
        self,
        page_size: int = 100,
        page_token: str | None = None,
        *,
        order_by: str = "",
        filter: str = "",
    ) -> PagingResult[PredictionModel]:
        """List metadata, defaulting to numeric model ID descending.

        Keep order_by and filter unchanged across pages. Filters support display_name
        and folder equalities joined with AND; display names support * wildcards.
        """
        response = self.client.list_models(
            ListPredictionModelsRequest(
                page_size=page_size, page_token=page_token, order_by=order_by, filter=filter
            )
        )
        return PagingResult(
            [PredictionModel.from_proto(m) for m in response.models],
            response.next_page_token,
            response.total_size,
        )

    def create_model(self, model: PredictionModel, folder: str | None = None) -> PredictionModel:
        """Save a model configuration without running it. Do not automatically retry creation."""
        response = self.client.create_model(
            CreatePredictionModelRequest(model=model.to_proto(), folder=folder)
        )
        return PredictionModel.from_proto(response)

    def update_model(
        self, model: PredictionModel, *, update_mask: Sequence[str]
    ) -> PredictionModel:
        """Replace only masked fields, including explicit empty values and False."""
        if isinstance(update_mask, str) or not update_mask:
            raise ValueError("update_mask must be a nonempty sequence of field paths")
        response = self.client.update_model(
            UpdatePredictionModelRequest(
                model=model.to_proto(), update_mask=FieldMask(paths=update_mask)
            )
        )
        return PredictionModel.from_proto(response)

    def get_run(self, name: str) -> PredictionModelRun | None:
        """Inspect the exact run resource returned by create_run."""
        try:
            response = self.client.get_run(GetPredictionModelRunRequest(name=name))
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise
        return PredictionModelRun.from_proto(response)

    def list_runs(
        self, model: str, page_size: int = 100, page_token: str | None = None
    ) -> PagingResult[PredictionModelRun]:
        """
        List regular run metadata newest first; get_run also returns its configuration.

        The server does not count runs, so total_size is always 0.
        """
        response = self.client.list_runs(
            ListPredictionModelRunsRequest(parent=model, page_size=page_size, page_token=page_token)
        )
        return PagingResult(
            [PredictionModelRun.from_proto(r) for r in response.runs], response.next_page_token, 0
        )

    def get_model_iterator(
        self, *, order_by: str = "", filter: str = ""
    ) -> Iterator[PredictionModel]:
        """Follow continuation tokens, including tokens returned with a short page."""
        token = None
        while True:
            page = self.list_models(page_token=token, order_by=order_by, filter=filter)
            yield from page.results
            if not page.next_page_token:
                return
            token = page.next_page_token

    def get_run_iterator(self, model: str) -> Iterator[PredictionModelRun]:
        """Iterate a model's history without substituting the currently active run."""
        token = None
        while True:
            page = self.list_runs(model, page_token=token)
            yield from page.results
            if not page.next_page_token:
                return
            token = page.next_page_token
