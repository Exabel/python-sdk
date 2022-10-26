from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.time_series_api import TimeSeriesApi
from exabel_data_sdk.tests.client.api.mock_entity_api import MockEntityApi
from exabel_data_sdk.tests.client.api.mock_relationship_api import MockRelationshipApi
from exabel_data_sdk.tests.client.api.mock_signal_api import MockSignalApi


class ExabelMockClient(ExabelClient):
    """
    Mock of the ExabelClient that uses mock implementations of the API classes,
    which only store objects in memory.
    """

    def __init__(self, namespace: str = "test"):  # pylint: disable=super-init-not-called
        self.entity_api = MockEntityApi()
        self.relationship_api = MockRelationshipApi()
        self.signal_api = MockSignalApi()
        self.time_series_api = mock.create_autospec(TimeSeriesApi)
        self._namespace = namespace
