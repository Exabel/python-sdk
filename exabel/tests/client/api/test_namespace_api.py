from unittest import mock

import pytest

from exabel.client.api.data_classes.namespace import Namespace
from exabel.client.api.namespace_api import NamespaceApi
from exabel.client.client_config import ClientConfig
from exabel.util.exceptions import NoWriteableNamespaceError


class TestNamespaceApi:
    @mock.patch("exabel.client.api.namespace_api.NamespaceApi.list_namespaces")
    def test_get_writeable_namespace(self, mock_list_namespaces):
        namespace_api = NamespaceApi(ClientConfig(api_key="123"))
        mock_list_namespaces.return_value = [
            Namespace(name="namespaces/ns1", writeable=True),
            Namespace(name="namespaces/ns2", writeable=False),
        ]
        assert (
            Namespace(name="namespaces/ns1", writeable=True)
            == namespace_api.get_writeable_namespace()
        )

    @mock.patch("exabel.client.api.namespace_api.NamespaceApi.list_namespaces")
    def test_get_writeable_namespace__no_writable_namespace_should_fail(self, mock_list_namespaces):
        namespace_api = NamespaceApi(ClientConfig(api_key="123"))
        mock_list_namespaces.return_value = [
            Namespace(name="namespaces/ns1", writeable=False),
            Namespace(name="namespaces/ns2", writeable=False),
        ]
        with pytest.raises(NoWriteableNamespaceError) as cm:
            namespace_api.get_writeable_namespace()
        assert "Current customer is not authorized to write to any namespace." == str(cm.value)

    @mock.patch("exabel.client.api.namespace_api.NamespaceApi.list_namespaces")
    def test_get_writeable_namespace__multiple_writeable_namespaces_should_log_warning(
        self, mock_list_namespaces, caplog
    ):
        namespace_api = NamespaceApi(ClientConfig(api_key="123"))
        mock_list_namespaces.return_value = [
            Namespace(name="namespaces/ns1", writeable=True),
            Namespace(name="namespaces/ns2", writeable=True),
        ]
        with caplog.at_level("WARNING", logger="exabel.client.api.namespace_api"):
            namespace_api.get_writeable_namespace()
        assert (
            "Current customer is authorized to write to 2 namespaces. Using the first lexicographical result: 'namespaces/ns1'."
            in caplog.text
        )
