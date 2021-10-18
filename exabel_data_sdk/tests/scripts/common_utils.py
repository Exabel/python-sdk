from typing import Sequence, Type

from exabel_data_sdk.client.exabel_client import ExabelClient
from exabel_data_sdk.scripts.csv_script import CsvScript
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient


def load_test_data_from_csv(csv_script: Type[CsvScript], args: Sequence[str]) -> ExabelClient:
    """Loads entities to an ExabelMockClient using exabel_data_sdk.scripts.load_entities_from_csv"""
    script = csv_script(args, f"Test{type(csv_script).__name__}")
    client = ExabelMockClient()
    script.run_script(client, script.parse_arguments())

    return client
