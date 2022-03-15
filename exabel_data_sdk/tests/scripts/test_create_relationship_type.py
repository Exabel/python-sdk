import unittest
from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.create_relationship_type import CreateRelationshipType

common_args = [
    "script-name",
    "--api-key",
    "123",
    "--name",
    "relationshipTypes/acme.MY_TEST_RELATIONSHIP",
]


class TestCreateRelationshipType(unittest.TestCase):
    def test_create_relationship_description_and_ownership(self):
        args = common_args + [
            "--description",
            "My description.",
            "--is-ownership",
        ]
        script = CreateRelationshipType(args, "Create a relationship type.")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())
        call_args_list = client.relationship_api.create_relationship_type.call_args_list
        self.assertEqual(call_args_list[0][0][0].description, "My description.")
        self.assertEqual(call_args_list[0][0][0].is_ownership, True)

    def test_create_relationship_no_ownership(self):
        args = common_args + [
            "--no-is-ownership",
        ]
        script = CreateRelationshipType(args, "Create a relationship type.")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())
        call_args_list = client.relationship_api.create_relationship_type.call_args_list
        self.assertEqual(call_args_list[0][0][0].description, None)
        self.assertEqual(call_args_list[0][0][0].is_ownership, False)

    def test_create_relationship_not_specified_ownership(self):
        args = common_args
        script = CreateRelationshipType(args, "Create a relationship type.")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        with self.assertRaises(SystemExit):
            script.run_script(client, script.parse_arguments())


if __name__ == "__main__":
    unittest.main()
