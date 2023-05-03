import unittest

from exabel_data_sdk.client.api.data_classes.prediction_model_run import (
    ModelConfiguration,
    PredictionModelRun,
)


class TestModelRun(unittest.TestCase):
    def test_proto_conversion(self):
        model_run = PredictionModelRun(
            name="predictionModels/123/runs/4",
            description="Test run",
            configuration=ModelConfiguration.SPECIFIC_RUN,
            configuration_source="predictionModels/123/runs/2",
            auto_activate=True,
        )
        self.assertEqual(model_run, PredictionModelRun.from_proto(model_run.to_proto()))
