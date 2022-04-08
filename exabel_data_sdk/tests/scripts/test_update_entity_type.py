import unittest
from unittest import mock

from google.protobuf.field_mask_pb2 import FieldMask

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.scripts.update_entity_type import UpdateEntityType

common_args = [
    "script-name",
    "--api-key",
    "123",
    "--name",
    "entityTypes/acme.entity_type",
]


class TestUpdateEntityType(unittest.TestCase):
    def test_update_entity_type(self):
        args = common_args + [
            "--display-name",
            "The display name",
            "--description",
            "The description.",
            "--is-associative",
        ]
        script = UpdateEntityType(args, "Update an entity type.")
        mock_client = mock.create_autospec(ExabelClient(api_key="123"))
        script.run_script(mock_client, script.parse_arguments())
        mock_client.entity_api.update_entity_type.assert_called_once_with(
            entity_type=EntityType(
                name="entityTypes/acme.entity_type",
                display_name="The display name",
                description="The description.",
                is_associative=True,
            ),
            update_mask=FieldMask(paths=["display_name", "description", "is_associative"]),
        )

    def test_update_entity_type_display_name_only(self):
        args = common_args + [
            "--display-name",
            "The display name",
        ]
        script = UpdateEntityType(args, "Update an entity type.")
        mock_client = mock.create_autospec(ExabelClient(api_key="123"))
        script.run_script(mock_client, script.parse_arguments())
        mock_client.entity_api.update_entity_type.assert_called_once_with(
            entity_type=EntityType(
                name="entityTypes/acme.entity_type",
                display_name="The display name",
                description="",
                is_associative=None,
            ),
            update_mask=FieldMask(paths=["display_name"]),
        )
