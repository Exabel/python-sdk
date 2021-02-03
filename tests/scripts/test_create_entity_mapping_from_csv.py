import unittest
from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.create_entity_mapping_from_csv import CreateEntityMappingFromCsv


class TestCreateEntityMappingFromCsv(unittest.TestCase):
    def test_file_format_error(self):
        args = [
            "script-name",
            "--filename-input",
            "./tests/resources/data/mapping_format_error.csv",
            "--filename-output",
            "s3://exabel-foursquare-test/data/etl-output/mapping/mapping_output.csv",
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTest1")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        with self.assertRaises(ValueError):
            script.run_script(client, script.parse_arguments())

    def test_create_mapping(self):

        args = [
            "script-name",
            "--filename-input",
            "./tests/resources/data/mapping.csv",
            "--filename-output",
            "s3://exabel-foursquare-test/data/etl-output/mapping/mapping_output.csv",
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTest2")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        # first call - entity = "entityType/company" ticker = "C" / market = "XNYS"
        call_args = client.entity_api.search_for_entities.call_args_list[0]
        cargs, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XNAS", "ticker": "C"},
            kwargs,
            "Arguments not as expected",
        )

        # second call - entity = "entityType/company" ticker = "C" / market = "XNAS"
        call_args = client.entity_api.search_for_entities.call_args_list[1]
        cargs, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XNYS", "ticker": "C"},
            kwargs,
            "Arguments not as expected",
        )
        # third call - entity = "entityType/company" ticker = "M" / market = "XNYS"
        call_args = client.entity_api.search_for_entities.call_args_list[2]
        cargs, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XNYS", "ticker": "M"},
            kwargs,
            "Arguments not as expected",
        )


if __name__ == "__main__":
    unittest.main()
