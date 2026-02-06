from exabel.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel.client.client_config import ClientConfig


class TestExabelApiGroup:
    def test_get_host(self):
        config = ClientConfig(api_key="123", data_api_host="localhost")
        assert "localhost" == ExabelApiGroup.DATA_API.get_host(config)
        assert "management.api.exabel.com" == ExabelApiGroup.MANAGEMENT_API.get_host(config)

    def test_get_port(self):
        config = ClientConfig(api_key="123", analytics_api_port=123)
        assert 123 == ExabelApiGroup.ANALYTICS_API.get_port(config)
        assert 21443 == ExabelApiGroup.MANAGEMENT_API.get_port(config)
