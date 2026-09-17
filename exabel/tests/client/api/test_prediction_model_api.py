from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
from google.protobuf.json_format import ParseDict

from exabel.client.api.data_classes.prediction_model import PredictionModel
from exabel.client.api.data_classes.prediction_model_run import (
    ModelConfiguration,
    PredictionModelRun,
    PredictionModelRunState,
)
from exabel.client.api.data_classes.request_error import ErrorType, RequestError
from exabel.client.api.prediction_model_api import PredictionModelApi
from exabel.stubs.exabel.api.analytics.v1 import prediction_model_messages_pb2 as messages
from exabel.stubs.exabel.api.analytics.v1 import prediction_model_service_pb2 as service


@pytest.fixture
def api():
    instance = PredictionModelApi.__new__(PredictionModelApi)
    instance.client = Mock()
    return instance


def configuration():
    return {
        "modelOptions": {
            "modelType": "ratio_prediction",
            "parameters": {"model": "uc_trend", "target_model": "none"},
        },
        "goal": "PREDICT",
        "targetSignals": [{"signal": {"id": 1}}],
        "predictorSignals": [{"signal": {"id": 2}, "modelParameters": {"monotone": True}}],
        "entities": [{"name": "entityTypes/company/entities/F_000C7F-E"}],
        "trainingDuration": {"base": "YEAR", "multiplier": 10},
        "hyperoptSettings": {"disableEnsemble": True, "level": "LEVEL_0"},
    }


def test_configuration_round_trip():
    original = PredictionModel("test", configuration())
    assert PredictionModel.from_proto(original.to_proto()).configuration == original.configuration


def test_unsupported_configuration_remains_inspectable():
    original = messages.PredictionModel(
        configuration_writable=False, configuration_error="modelType"
    )
    ParseDict(
        {"modelOptions": {"modelType": "auto", "parameters": {"unknown": [1, None, False]}}},
        original.configuration,
    )
    model = PredictionModel.from_proto(original)
    assert model.configuration["modelOptions"]["parameters"]["unknown"] == [1, None, False]
    assert model.configuration_writable is False
    assert not model.to_proto().HasField("configuration_writable")


def test_model_serializes_only_writable_fields():
    model = PredictionModel(
        "test",
        configuration(),
        "predictionModels/1",
        folder="folders/1",
        configuration_error="unsupported",
    )
    assert model.to_proto().folder == ""
    assert model.to_proto().configuration_error == ""


def test_update_preserves_mask_and_explicit_false(api):
    config = configuration()
    config["predictorSignals"][0]["modelParameters"]["monotone"] = False
    model = PredictionModel("test", config, "predictionModels/1")
    api.client.update_model.return_value = model.to_proto()
    api.update_model(model, update_mask=["configuration.predictor_signals"])
    request = api.client.update_model.call_args.args[0]
    assert request.update_mask.paths == ["configuration.predictor_signals"]
    assert not request.model.configuration.predictor_signals[0].model_parameters.monotone


def test_model_iterator_follows_short_page_token(api):
    api.client.list_models.side_effect = [
        service.ListPredictionModelsResponse(
            models=[messages.PredictionModel(name="predictionModels/1")],
            next_page_token="next",
            total_size=2,
        ),
        service.ListPredictionModelsResponse(
            models=[messages.PredictionModel(name="predictionModels/2")], total_size=2
        ),
    ]
    assert [model.name for model in api.get_model_iterator()] == [
        "predictionModels/1",
        "predictionModels/2",
    ]
    assert api.client.list_models.call_args.args[0].page_token == "next"


def test_run_readback_with_unspecified_request_options(api):
    api.client.get_run.return_value = messages.PredictionModelRun(
        name="predictionModels/1/runs/4", state=messages.FAILED, error="Insufficient data"
    )
    run = api.get_run("predictionModels/1/runs/4")
    assert api.client.get_run.call_args.args[0].name == "predictionModels/1/runs/4"
    assert run.configuration == ModelConfiguration.UNSPECIFIED
    assert run.state == PredictionModelRunState.FAILED
    assert run.error == "Insufficient data"
    assert run.create_time is None


def test_run_output_fields_are_not_sent_to_create():
    run = PredictionModelRun.from_proto(
        messages.PredictionModelRun(
            name="predictionModels/1/runs/4", state=messages.FAILED, error="Insufficient data"
        )
    )
    assert run.to_proto().state == 0
    assert run.to_proto().error == ""


def test_unknown_run_state_is_preserved():
    run = PredictionModelRun.from_proto(messages.PredictionModelRun(state=500))
    assert run.state == 500


@pytest.mark.parametrize("method", ["get_model", "get_run"])
def test_get_returns_none_only_for_not_found(api, method):
    from exabel.client.api.data_classes.request_error import ErrorType, RequestError

    getattr(api.client, method).side_effect = RequestError(ErrorType.NOT_FOUND)
    assert getattr(api, method)("resource") is None
    getattr(api.client, method).side_effect = RequestError(ErrorType.PERMISSION_DENIED)
    with pytest.raises(RequestError):
        getattr(api, method)("resource")


def test_create_sends_folder_without_response_fields(api):
    model = PredictionModel("candidate", configuration(), folder="folders/999")
    api.client.create_model.return_value = model.to_proto()
    api.create_model(model, folder="folders/123")
    request = api.client.create_model.call_args.args[0]
    assert request.folder == "folders/123"
    assert (
        request.model.configuration
        == PredictionModel("candidate", configuration()).to_proto().configuration
    )
    assert request.model.folder == ""


def test_run_iterator_follows_empty_page_token(api):
    api.client.list_runs.side_effect = [
        service.ListPredictionModelRunsResponse(next_page_token="next"),
        service.ListPredictionModelRunsResponse(
            runs=[messages.PredictionModelRun(name="predictionModels/1/runs/2")]
        ),
    ]
    assert [run.name for run in api.get_run_iterator("predictionModels/1")] == [
        "predictionModels/1/runs/2"
    ]
    request = api.client.list_runs.call_args.args[0]
    assert request.parent == "predictionModels/1"
    assert request.page_token == "next"


@pytest.mark.parametrize("mask", [[], "description"])
def test_invalid_mask_is_rejected_before_rpc(api, mask):
    with pytest.raises(ValueError):
        api.update_model(PredictionModel("candidate"), update_mask=mask)
    api.client.update_model.assert_not_called()


def test_delete_model_sends_resource_name(api):
    assert api.delete_model("predictionModels/123") is None
    api.client.delete_model.assert_called_once_with(
        service.DeletePredictionModelRequest(name="predictionModels/123")
    )


def test_delete_model_preserves_permission_error(api):
    error = RequestError(ErrorType.PERMISSION_DENIED)
    api.client.delete_model.side_effect = error
    with pytest.raises(RequestError) as raised:
        api.delete_model("predictionModels/123")
    assert raised.value is error


def test_run_entity_outcomes_and_timestamp():
    from google.protobuf.timestamp_pb2 import Timestamp

    run = PredictionModelRun.from_proto(
        messages.PredictionModelRun(
            state=messages.MIXED,
            create_time=Timestamp(seconds=100),
            entity_outcomes=[
                messages.PredictionModelEntityOutcome(
                    entity="entityTypes/company/entities/F_000C7F-E",
                    state=messages.FAILED,
                    error="No data",
                )
            ],
        )
    )
    assert run.create_time == datetime.fromtimestamp(100, tz=timezone.utc)
    assert run.entity_outcomes[0].state == PredictionModelRunState.FAILED
    assert run.entity_outcomes[0].error == "No data"


@pytest.mark.parametrize(
    ("method", "rpc", "request_type"),
    [
        ("get_model", "GetPredictionModel", service.GetPredictionModelRequest),
        ("list_models", "ListPredictionModels", service.ListPredictionModelsRequest),
        ("create_model", "CreatePredictionModel", service.CreatePredictionModelRequest),
        ("update_model", "UpdatePredictionModel", service.UpdatePredictionModelRequest),
        ("delete_model", "DeletePredictionModel", service.DeletePredictionModelRequest),
        ("get_run", "GetPredictionModelRun", service.GetPredictionModelRunRequest),
        ("list_runs", "ListPredictionModelRuns", service.ListPredictionModelRunsRequest),
    ],
)
def test_transport_preserves_credentials_and_timeout(method, rpc, request_type):
    from exabel.client.api.api_client.grpc.prediction_model_grpc_client import (
        PredictionModelGrpcClient,
    )

    client = PredictionModelGrpcClient.__new__(PredictionModelGrpcClient)
    client.stub = Mock()
    client.metadata = [("x-api-key", "test-key")]
    client.config = Mock(timeout=12)
    request = request_type()
    getattr(client, method)(request)
    getattr(client.stub, rpc).assert_called_once_with(request, metadata=client.metadata, timeout=12)


def test_transport_does_not_retry_creation_but_retries_reads():
    from concurrent.futures import ThreadPoolExecutor

    import grpc

    from exabel.client.api.api_client.grpc.prediction_model_grpc_client import (
        PredictionModelGrpcClient,
    )
    from exabel.client.api.data_classes.request_error import RequestError
    from exabel.stubs.exabel.api.analytics.v1.prediction_model_service_pb2_grpc import (
        PredictionModelServiceServicer,
        PredictionModelServiceStub,
        add_PredictionModelServiceServicer_to_server,
    )

    class FailingService(PredictionModelServiceServicer):
        creates = 0
        run_creates = 0
        reads = 0

        def CreatePredictionModel(self, request, context):
            self.creates += 1
            context.abort(grpc.StatusCode.UNAVAILABLE, "Ambiguous creation failure")

        def CreatePredictionModelRun(self, request, context):
            self.run_creates += 1
            context.abort(grpc.StatusCode.UNAVAILABLE, "Ambiguous run creation failure")

        def GetPredictionModel(self, request, context):
            self.reads += 1
            if self.reads == 1:
                context.abort(grpc.StatusCode.UNAVAILABLE, "Transient read failure")
            return messages.PredictionModel(name=request.name)

    implementation = FailingService()
    with ThreadPoolExecutor(max_workers=2) as executor:
        server = grpc.server(executor)
        add_PredictionModelServiceServicer_to_server(implementation, server)
        port = server.add_insecure_port("127.0.0.1:0")
        server.start()
        client = PredictionModelGrpcClient.__new__(PredictionModelGrpcClient)
        client.config = Mock(timeout=2)
        client.metadata = []
        try:
            with grpc.insecure_channel(
                f"127.0.0.1:{port}", options=[("grpc.service_config", client._get_service_config())]
            ) as channel:
                client.stub = PredictionModelServiceStub(channel)
                with pytest.raises(RequestError):
                    client.create_model(service.CreatePredictionModelRequest())
                assert implementation.creates == 1
                with pytest.raises(RequestError):
                    client.create_model_run(service.CreatePredictionModelRunRequest())
                assert implementation.run_creates == 1
                assert (
                    client.get_model(
                        service.GetPredictionModelRequest(name="predictionModels/1")
                    ).name
                    == "predictionModels/1"
                )
                assert implementation.reads == 2
        finally:
            server.stop(None).wait()


@pytest.mark.parametrize("left", [None, False, True])
@pytest.mark.parametrize("right", [None, False, True])
def test_run_equality_includes_configuration_writability(left, right):
    first = PredictionModelRun(name="predictionModels/1/runs/1", model_configuration_writable=left)
    second = PredictionModelRun(
        name="predictionModels/1/runs/1", model_configuration_writable=right
    )
    assert (first == second) == (left == right)


def test_model_discovery_options_persist_across_pages(api):
    api.client.list_models.side_effect = [
        service.ListPredictionModelsResponse(next_page_token="next"),
        service.ListPredictionModelsResponse(),
    ]
    assert (
        list(api.get_model_iterator(order_by="update_time desc", filter='folder="folders/123"'))
        == []
    )
    for call in api.client.list_models.call_args_list:
        assert call.args[0].order_by == "update_time desc"
        assert call.args[0].filter == 'folder="folders/123"'
    assert api.client.list_models.call_args.args[0].page_token == "next"


def test_model_timestamps_are_read_only():
    value = messages.PredictionModel(display_name="model")
    value.create_time.FromJsonString("2024-01-01T00:00:00Z")
    value.update_time.FromJsonString("2024-02-01T00:00:00Z")
    model = PredictionModel.from_proto(value)
    assert model.create_time == datetime(2024, 1, 1, tzinfo=timezone.utc)
    assert model.update_time == datetime(2024, 2, 1, tzinfo=timezone.utc)
    assert not model.to_proto().HasField("create_time")
    assert not model.to_proto().HasField("update_time")


@pytest.mark.parametrize("source", [None, 0])
def test_specific_run_readback_preserves_source_presence(api, source):
    proto = messages.PredictionModelRun(
        name="predictionModels/1/runs/2",
        configuration=messages.SPECIFIC_RUN,
        configuration_source=source,
    )
    api.client.get_run.return_value = proto
    api.client.list_runs.return_value = service.ListPredictionModelRunsResponse(
        runs=[proto, messages.PredictionModelRun(name="predictionModels/1/runs/3")]
    )
    run = api.get_run(proto.name)
    assert run.configuration == ModelConfiguration.SPECIFIC_RUN
    assert run.configuration_source == source
    runs = list(api.get_run_iterator("predictionModels/1"))
    assert len(runs) == 2
    assert runs[0].configuration_source == source


def test_missing_specific_run_source_is_rejected_before_rpc(api):
    run = PredictionModelRun(configuration=ModelConfiguration.SPECIFIC_RUN)
    with pytest.raises(ValueError, match="configuration_source"):
        api.create_run(run, "predictionModels/1")
    api.client.create_model_run.assert_not_called()


def test_specific_run_source_zero_round_trips():
    run = PredictionModelRun(configuration=ModelConfiguration.SPECIFIC_RUN, configuration_source=0)
    proto = run.to_proto()
    assert proto.HasField("configuration_source")
    assert PredictionModelRun.from_proto(proto).configuration_source == 0
