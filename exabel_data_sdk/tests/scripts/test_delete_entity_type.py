import unittest
from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.scripts.delete_entity_type import DeleteEntityType

common_args = [
    "script-name",
    "--api-key",
    "123",
    "--name",
    "entityTypes/acme.entity_type",
]


class TestdeleteEntityType(unittest.TestCase):
    def test_delete_entity_type(self):
        script = DeleteEntityType(common_args, "Delete an entity type.")
        mock_client = mock.create_autospec(ExabelClient)
        mock_client.entity_api = mock.create_autospec(EntityApi)
        script.run_script(mock_client, script.parse_arguments())
        mock_client.entity_api.delete_entity_type.assert_called_once_with(
            name="entityTypes/acme.entity_type"
        )
