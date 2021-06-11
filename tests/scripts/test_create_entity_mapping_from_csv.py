import tempfile
import unittest
from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.create_entity_mapping_from_csv import CreateEntityMappingFromCsv


class TestCreateEntityMappingFromCsv(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile()  # pylint: disable=consider-using-with

    def tearDown(self):
        self.temp_file.close()

    def test_create_mapping_ticker(self):

        args = [
            "script-name",
            "--filename-input",
            "./tests/resources/data/mapping_ticker.csv",
            "--filename-output",
            self.temp_file.name,
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTest2")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        # first call - entity = "entityType/company" ticker = "C" / market = "XNYS"
        call_args = client.entity_api.search_for_entities.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XNAS", "ticker": "C"},
            kwargs,
            "Arguments not as expected",
        )

        # second call - entity = "entityType/company" ticker = "C" / market = "XNAS"
        call_args = client.entity_api.search_for_entities.call_args_list[1]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XNYS", "ticker": "C"},
            kwargs,
            "Arguments not as expected",
        )

        # third call - entity = "entityType/company" ticker = "M" / market = "XNYS"
        call_args = client.entity_api.search_for_entities.call_args_list[2]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XNYS", "ticker": "M"},
            kwargs,
            "Arguments not as expected",
        )

    def test_create_mapping_isin(self):

        args = [
            "script-name",
            "--filename-input",
            "./tests/resources/data/mapping_isin.csv",
            "--filename-output",
            self.temp_file.name,
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTestISIN")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        # first call - entity = "entityType/company" isin = 'NO12345678'
        call_args = client.entity_api.search_for_entities.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "isin": "NO0010096985"},
            kwargs,
            "Arguments not as expected",
        )

    def test_create_mapping_factset_identifier(self):

        args = [
            "script-name",
            "--filename-input",
            "./tests/resources/data/mapping_factset_identifier.csv",
            "--filename-output",
            self.temp_file.name,
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTestISIN")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        # first call - entity = "entityType/company" factset_identifier = '0MXNWD-E'
        call_args = client.entity_api.search_for_entities.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "factset_identifier": "0MXNWD-E"},
            kwargs,
            "Arguments not as expected",
        )

        # second call - entity = "entityType/company" factset_identifier = 'DT699H-S'
        call_args = client.entity_api.search_for_entities.call_args_list[1]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "factset_identifier": "DT699H-S"},
            kwargs,
            "Arguments not as expected",
        )

    def test_create_mapping_bloomberg_ticker(self):

        args = [
            "script-name",
            "--filename-input",
            "./tests/resources/data/mapping_bloomberg_ticker.csv",
            "--filename-output",
            self.temp_file.name,
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTestISIN")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        # first call - entity = "entityType/company" bloomberg_ticker = 'AAPL US'
        call_args = client.entity_api.search_for_entities.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "bloomberg_ticker": "AAPL US"},
            kwargs,
            "Arguments not as expected",
        )

        # second call - entity = "entityType/company" factset_identifier = 'DT699H-S'
        call_args = client.entity_api.search_for_entities.call_args_list[1]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "bloomberg_ticker": "AMZN US"},
            kwargs,
            "Arguments not as expected",
        )


if __name__ == "__main__":
    unittest.main()
