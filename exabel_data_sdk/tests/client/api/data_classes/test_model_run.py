import unittest

from exabel_data_sdk.client.api.data_classes.model_run import ModelRun


class TestModelRun(unittest.TestCase):
    def test_proto_conversion(self):
        model_run = ModelRun(
            name="models/123/runs/4",
            description="Test run",
        )
        self.assertEqual(model_run, ModelRun.from_proto(model_run.to_proto()))
