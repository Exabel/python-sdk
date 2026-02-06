from exabel.client.client_config import ClientConfig


class TestExabelClient:
    def test_default_config(self):
        config = ClientConfig(api_key="123")
        assert "123" == config.api_key
        assert "Exabel Python SDK" == config.client_name
        assert "data.api.exabel.com" == config.data_api_host
        assert "analytics.api.exabel.com" == config.analytics_api_host
        assert "management.api.exabel.com" == config.management_api_host
        assert 21443 == config.data_api_port
        assert 60 * 15 == config.timeout

    def test_non_default_values(self):
        config = ClientConfig(
            api_key="123",
            client_name="my client",
            data_api_host="foo.bar.com",
            data_api_port=1234,
            timeout=45,
        )
        assert "123" == config.api_key
        assert "my client" == config.client_name
        assert "foo.bar.com" == config.data_api_host
        assert 1234 == config.data_api_port
        assert 45 == config.timeout
