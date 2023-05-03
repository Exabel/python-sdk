import unittest

from exabel_data_sdk.client.api.data_classes.prediction_model_run import (
    ModelConfiguration,
    PredictionModelRun,
)


class TestModelRun(unittest.TestCase):
    def test_proto_conversion__with_configuration_source(self):
        model_run = PredictionModelRun(
            name="predictionModels/123/runs/4",
            description="Test run",
            configuration=ModelConfiguration.SPECIFIC_RUN,
            configuration_source=2,
            auto_activate=True,
        )
        self.assertEqual(model_run, PredictionModelRun.from_proto(model_run.to_proto()))

    def test_proto_conversion__without_configuration_source(self):
        model_run = PredictionModelRun(
            name="predictionModels/123/runs/4",
            description="Test run",
            configuration=ModelConfiguration.ACTIVE,
        )
        self.assertEqual(model_run, PredictionModelRun.from_proto(model_run.to_proto()))
