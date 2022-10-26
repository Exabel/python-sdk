import unittest
from unittest import mock

from exabel_data_sdk.client.api.data_classes.namespace import Namespace
from exabel_data_sdk.client.api.namespace_api import NamespaceApi
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.util.exceptions import NoWriteableNamespaceError


class TestNamespaceApi(unittest.TestCase):
    @mock.patch("exabel_data_sdk.client.api.namespace_api.NamespaceApi.list_namespaces")
    def test_get_writeable_namespace(self, mock_list_namespaces):
        namespace_api = NamespaceApi(ClientConfig(api_key="123"))
        mock_list_namespaces.return_value = [
            Namespace(name="namespaces/ns1", writeable=True),
            Namespace(name="namespaces/ns2", writeable=False),
        ]
        self.assertEqual(
            Namespace(name="namespaces/ns1", writeable=True),
            namespace_api.get_writeable_namespace(),
        )

    @mock.patch("exabel_data_sdk.client.api.namespace_api.NamespaceApi.list_namespaces")
    def test_get_writeable_namespace__no_writable_namespace_should_fail(self, mock_list_namespaces):
        namespace_api = NamespaceApi(ClientConfig(api_key="123"))
        mock_list_namespaces.return_value = [
            Namespace(name="namespaces/ns1", writeable=False),
            Namespace(name="namespaces/ns2", writeable=False),
        ]
        with self.assertRaises(NoWriteableNamespaceError) as cm:
            namespace_api.get_writeable_namespace()
        self.assertEqual(
            "Current customer is not authorized to write to any namespace.", str(cm.exception)
        )

    @mock.patch("exabel_data_sdk.client.api.namespace_api.NamespaceApi.list_namespaces")
    def test_get_writeable_namespace__multiple_writeable_namespaces_should_log_warning(
        self, mock_list_namespaces
    ):
        namespace_api = NamespaceApi(ClientConfig(api_key="123"))
        mock_list_namespaces.return_value = [
            Namespace(name="namespaces/ns1", writeable=True),
            Namespace(name="namespaces/ns2", writeable=True),
        ]
        with self.assertLogs("exabel_data_sdk.client.api.namespace_api", "WARNING") as cm:
            namespace_api.get_writeable_namespace()
        self.assertEqual(
            "WARNING:exabel_data_sdk.client.api.namespace_api:Current customer is authorized to "
            "write to 2 namespaces. Using the first lexicographical result: 'namespaces/ns1'.",
            str(cm.output[0]),
        )
