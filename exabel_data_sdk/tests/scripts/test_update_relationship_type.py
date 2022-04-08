import unittest
from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.update_relationship_type import UpdateRelationshipType

common_args = [
    "script-name",
    "--api-key",
    "123",
    "--name",
    "relationshipTypes/acme.MY_TEST_RELATIONSHIP",
]


class TestUpdateRelationshipType(unittest.TestCase):
    def test_update_description(self):
        args = common_args + [
            "--description",
            "My updated description.",
        ]
        script = UpdateRelationshipType(args, "Update a relationship type.")
        client = mock.create_autospec(ExabelClient(api_key="123"))
        script.run_script(client, script.parse_arguments())
        call_args_list = client.relationship_api.update_relationship_type.call_args_list
        update_mask = call_args_list[0][1]["update_mask"].paths

        self.assertEqual(call_args_list[0][0][0].description, "My updated description.")
        self.assertSetEqual({"description"}, set(update_mask))

    def test_update_is_ownership(self):
        args = common_args + [
            "--is-ownership",
        ]
        script = UpdateRelationshipType(args, "Update a relationship type.")
        client = mock.create_autospec(ExabelClient(api_key="123"))
        script.run_script(client, script.parse_arguments())
        call_args_list = client.relationship_api.update_relationship_type.call_args_list
        update_mask = call_args_list[0][1]["update_mask"].paths

        self.assertEqual(call_args_list[0][0][0].is_ownership, True)
        self.assertSetEqual({"is_ownership"}, set(update_mask))

    def test_update_no_is_ownership(self):
        args = common_args + [
            "--no-is-ownership",
        ]
        script = UpdateRelationshipType(args, "Update a relationship type.")
        client = mock.create_autospec(ExabelClient(api_key="123"))
        script.run_script(client, script.parse_arguments())
        call_args_list = client.relationship_api.update_relationship_type.call_args_list
        update_mask = call_args_list[0][1]["update_mask"].paths

        self.assertEqual(call_args_list[0][0][0].is_ownership, False)
        self.assertSetEqual({"is_ownership"}, set(update_mask))

    def test_allow_missing(self):
        args = common_args + [
            "--allow-missing",
        ]
        script = UpdateRelationshipType(args, "Update a relationship type.")
        client = mock.create_autospec(ExabelClient(api_key="123"))
        script.run_script(client, script.parse_arguments())
        call_args_list = client.relationship_api.update_relationship_type.call_args_list
        allow_missing = call_args_list[0][1]["allow_missing"]

        self.assertEqual(allow_missing, True)


if __name__ == "__main__":
    unittest.main()
