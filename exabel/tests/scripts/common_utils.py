from typing import Sequence

from exabel.client.exabel_client import ExabelClient
from exabel.scripts.csv_script import CsvScript
from exabel.tests.client.exabel_mock_client import ExabelMockClient


def load_test_data_from_csv(
    csv_script: type[CsvScript],
    args: Sequence[str],
    client: ExabelClient | None = None,
    namespace: str = "test",
) -> ExabelClient:
    """Loads resources to an ExabelMockClient using CsvScript"""
    script = csv_script(args, f"Test{type(csv_script).__name__}")
    client = client or ExabelMockClient(namespace=namespace)
    script.run_script(client, script.parse_arguments())

    return client
