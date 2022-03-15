from typing import Sequence, Type

from exabel_data_sdk.client.exabel_client import ExabelClient
from exabel_data_sdk.scripts.csv_script import CsvScript
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient


def load_test_data_from_csv(
    csv_script: Type[CsvScript], args: Sequence[str], client: ExabelClient = None
) -> ExabelClient:
    """Loads resources to an ExabelMockClient using CsvScript"""
    script = csv_script(args, f"Test{type(csv_script).__name__}")
    client = client or ExabelMockClient()
    script.run_script(client, script.parse_arguments())

    return client
