import unittest

from exabel_data_sdk.client.api.data_classes.prediction_model_run import PredictionModelRun


class TestModelRun(unittest.TestCase):
    def test_proto_conversion(self):
        model_run = PredictionModelRun(
            name="predictionModels/123/runs/4",
            description="Test run",
        )
        self.assertEqual(model_run, PredictionModelRun.from_proto(model_run.to_proto()))
