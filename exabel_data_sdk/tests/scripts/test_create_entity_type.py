import unittest
from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.scripts.create_entity_type import CreateEntityType

common_args = [
    "script-name",
    "--api-key",
    "123",
    "--name",
    "entityTypes/acme.entity_type",
]


class TestCreateEntityType(unittest.TestCase):
    def test_create_entity_type(self):
        args = common_args + [
            "--display-name",
            "The display name",
            "--description",
            "The description.",
            "--no-is-associative",
        ]
        script = CreateEntityType(args, "Create an entity type.")
        mock_client = mock.create_autospec(ExabelClient(api_key="123"))
        script.run_script(mock_client, script.parse_arguments())
        mock_client.entity_api.create_entity_type.assert_called_once_with(
            EntityType(
                name="entityTypes/acme.entity_type",
                display_name="The display name",
                description="The description.",
                is_associative=False,
            )
        )

    def test_create_entity_type_should_fail(self):
        args = common_args + [
            "--display-name",
            "The display name",
            "--description",
            "The description.",
        ]
        script = CreateEntityType(args, "Create an entity type.")
        mock_client = mock.create_autospec(ExabelClient(api_key="123"))
        with self.assertRaises(SystemExit) as cm:
            script.run_script(mock_client, script.parse_arguments())
        self.assertEqual(2, cm.exception.code)
