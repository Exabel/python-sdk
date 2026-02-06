import unittest
from unittest import mock

import pytest

from exabel import ExabelClient
from exabel.client.api.relationship_api import RelationshipApi
from exabel.scripts.create_relationship_type import CreateRelationshipType

common_args = [
    "script-name",
    "--api-key",
    "123",
    "--name",
    "relationshipTypes/acme.MY_TEST_RELATIONSHIP",
]


class TestCreateRelationshipType(unittest.TestCase):
    def setUp(self) -> None:
        self.client = mock.create_autospec(ExabelClient)
        self.client.relationship_api = mock.create_autospec(RelationshipApi)

    def test_create_relationship_description_and_ownership(self):
        args = common_args + [
            "--description",
            "My description.",
            "--is-ownership",
        ]
        script = CreateRelationshipType(args, "Create a relationship type.")
        script.run_script(self.client, script.parse_arguments())
        call_args_list = self.client.relationship_api.create_relationship_type.call_args_list
        assert call_args_list[0][0][0].description == "My description."
        assert call_args_list[0][0][0].is_ownership

    def test_create_relationship_no_ownership(self):
        args = common_args + [
            "--no-is-ownership",
        ]
        script = CreateRelationshipType(args, "Create a relationship type.")
        script.run_script(self.client, script.parse_arguments())
        call_args_list = self.client.relationship_api.create_relationship_type.call_args_list
        assert call_args_list[0][0][0].description is None
        assert not call_args_list[0][0][0].is_ownership

    def test_create_relationship_not_specified_ownership(self):
        args = common_args
        script = CreateRelationshipType(args, "Create a relationship type.")
        with pytest.raises(SystemExit):
            script.run_script(self.client, script.parse_arguments())
