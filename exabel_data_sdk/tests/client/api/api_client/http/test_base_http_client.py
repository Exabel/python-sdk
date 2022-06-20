import json
import unittest
from unittest import mock
from unittest.mock import MagicMock

from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import Signal

# pylint: disable=protected-access


class TestBaseHttpClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = BaseHttpClient(
            ClientConfig(data_api_host="the-host", api_key="something"), ExabelApiGroup.DATA_API
        )

    @mock.patch("requests.request")
    def test_handle_successful_request(self, request):
        response = MagicMock()
        response.status_code = 200
        values = {"name": "signal-name"}
        response.content = json.dumps(values)
        request.return_value = response
        result = self.client._request("GET", "the-url", Signal(), body=Signal(name="input-signal"))
        self.assertEqual(Signal(name="signal-name"), result)

        request.assert_called_with(
            "GET",
            "https://the-host/v1/the-url",
            data='{\n  "name": "input-signal"\n}',
            headers={"Accept": "application/json", "X-Api-Key": "something"},
        )

    @mock.patch("requests.request")
    def test_handle_successful_request_without_body(self, request):
        response = MagicMock()
        response.status_code = 200
        values = {"name": "signal-name"}
        response.content = json.dumps(values)
        request.return_value = response
        result = self.client._request("GET", "the-url", Signal())
        self.assertEqual(Signal(name="signal-name"), result)

        request.assert_called_with(
            "GET",
            "https://the-host/v1/the-url",
            data=None,
            headers={"Accept": "application/json", "X-Api-Key": "something"},
        )

    @mock.patch("requests.request")
    def test_handle_successful_request_with_unknown_field_in_response(self, request):
        response = MagicMock()
        response.status_code = 200
        values = {"name": "signal-name", "unknown-field": "some-value"}
        response.content = json.dumps(values)
        request.return_value = response
        result = self.client._request("GET", "the-url", Signal())
        self.assertEqual(Signal(name="signal-name"), result)

    @mock.patch("requests.request")
    def test_handle_successful_request_without_response_object(self, request):
        response = MagicMock()
        response.status_code = 200
        request.return_value = response
        result = self.client._request("GET", "the-url", response_proto=None)
        self.assertIsNone(result)

    @mock.patch("requests.request")
    def test_handle_unsuccessful_request(self, request):
        response = MagicMock()
        response.status_code = 400
        values = {"message": "Something went wrong."}
        response.content = json.dumps(values)
        request.return_value = response
        with self.assertRaises(RequestError) as context:
            self.client._request("GET", "the-url", response_proto=None)
        self.assertEqual("Something went wrong.", str(context.exception.message))
