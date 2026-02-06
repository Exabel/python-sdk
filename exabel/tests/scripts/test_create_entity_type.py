import unittest
from unittest import mock

import pytest

from exabel import ExabelClient
from exabel.client.api.data_classes.entity_type import EntityType
from exabel.client.api.entity_api import EntityApi
from exabel.scripts.create_entity_type import CreateEntityType

common_args = [
    "script-name",
    "--api-key",
    "123",
    "--name",
    "entityTypes/acme.entity_type",
]


class TestCreateEntityType(unittest.TestCase):
    def setUp(self) -> None:
        self.client = mock.create_autospec(ExabelClient)
        self.client.entity_api = mock.create_autospec(EntityApi)

    def test_create_entity_type(self):
        args = common_args + [
            "--display-name",
            "The display name",
            "--description",
            "The description.",
            "--no-is-associative",
        ]
        script = CreateEntityType(args, "Create an entity type.")
        script.run_script(self.client, script.parse_arguments())
        self.client.entity_api.create_entity_type.assert_called_once_with(
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
        with pytest.raises(SystemExit) as exc_info:
            script.run_script(self.client, script.parse_arguments())
        assert 2 == exc_info.value.code
