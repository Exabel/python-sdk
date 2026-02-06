from unittest import mock

from exabel import ExabelClient
from exabel.client.api.data_classes.namespace import Namespace


class TestExabelClient:
    def test_initialize(self):
        client = ExabelClient(api_key="123")
        assert client.entity_api is not None
        assert client.time_series_api is not None
        assert client.relationship_api is not None
        assert client.signal_api is not None

    def test_namespace(self):
        client = ExabelClient(api_key="123")
        with mock.patch.object(client, "namespace_api") as mock_namespace_api:
            mock_namespace_api.get_writeable_namespace.return_value = Namespace(
                name="namespaces/ns", writeable=True
            )
            actual_namespace = client.namespace

        assert "ns" == actual_namespace
