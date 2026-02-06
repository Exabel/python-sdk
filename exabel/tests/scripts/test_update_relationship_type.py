from unittest import mock

import pytest

from exabel import ExabelClient
from exabel.client.api.relationship_api import RelationshipApi
from exabel.scripts.update_relationship_type import UpdateRelationshipType

common_args = [
    "script-name",
    "--api-key",
    "123",
    "--name",
    "relationshipTypes/acme.MY_TEST_RELATIONSHIP",
]


class TestUpdateRelationshipType:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.client = mock.create_autospec(ExabelClient)
        self.client.relationship_api = mock.create_autospec(RelationshipApi)

    def test_update_description(self):
        args = common_args + [
            "--description",
            "My updated description.",
        ]
        script = UpdateRelationshipType(args, "Update a relationship type.")
        script.run_script(self.client, script.parse_arguments())
        call_args_list = self.client.relationship_api.update_relationship_type.call_args_list
        update_mask = call_args_list[0][1]["update_mask"].paths

        assert call_args_list[0][0][0].description == "My updated description."
        assert set({"description"}) == set(set(update_mask))

    def test_update_is_ownership(self):
        args = common_args + [
            "--is-ownership",
        ]
        script = UpdateRelationshipType(args, "Update a relationship type.")
        script.run_script(self.client, script.parse_arguments())
        call_args_list = self.client.relationship_api.update_relationship_type.call_args_list
        update_mask = call_args_list[0][1]["update_mask"].paths

        assert call_args_list[0][0][0].is_ownership
        assert set({"is_ownership"}) == set(set(update_mask))

    def test_update_no_is_ownership(self):
        args = common_args + [
            "--no-is-ownership",
        ]
        script = UpdateRelationshipType(args, "Update a relationship type.")
        script.run_script(self.client, script.parse_arguments())
        call_args_list = self.client.relationship_api.update_relationship_type.call_args_list
        update_mask = call_args_list[0][1]["update_mask"].paths

        assert not call_args_list[0][0][0].is_ownership
        assert set({"is_ownership"}) == set(set(update_mask))

    def test_allow_missing(self):
        args = common_args + [
            "--allow-missing",
        ]
        script = UpdateRelationshipType(args, "Update a relationship type.")
        script.run_script(self.client, script.parse_arguments())
        call_args_list = self.client.relationship_api.update_relationship_type.call_args_list
        allow_missing = call_args_list[0][1]["allow_missing"]

        assert allow_missing
