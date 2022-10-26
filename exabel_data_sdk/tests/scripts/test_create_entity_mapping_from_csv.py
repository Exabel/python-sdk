import tempfile
import unittest
from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.scripts.create_entity_mapping_from_csv import CreateEntityMappingFromCsv


class TestCreateEntityMappingFromCsv(unittest.TestCase):
    def setUp(self):
        self.client = mock.create_autospec(ExabelClient)
        self.client.entity_api = mock.create_autospec(EntityApi)
        self.temp_file = tempfile.NamedTemporaryFile()  # pylint: disable=consider-using-with

    def tearDown(self):
        self.temp_file.close()

    def test_create_mapping_ticker(self):

        args = [
            "script-name",
            "--filename-input",
            "./exabel_data_sdk/tests/resources/data/mapping_ticker.csv",
            "--filename-output",
            self.temp_file.name,
            "--api-key",
            "123",
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTest2")
        script.run_script(self.client, script.parse_arguments())

        # first call - entity = "entityType/company" ticker = "C" / market = "XNYS"
        call_args = self.client.entity_api.search_for_entities.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XNAS", "ticker": "C"},
            kwargs,
            "Arguments not as expected",
        )

        # second call - entity = "entityType/company" ticker = "C" / market = "XNAS"
        call_args = self.client.entity_api.search_for_entities.call_args_list[1]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XNYS", "ticker": "C"},
            kwargs,
            "Arguments not as expected",
        )

        # third call - entity = "entityType/company" ticker = "C" / market = "XASE"
        call_args = self.client.entity_api.search_for_entities.call_args_list[2]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XASE", "ticker": "C"},
            kwargs,
            "Arguments not as expected",
        )

        # fourth call - entity = "entityType/company" ticker = "M" / market = "XNYS"
        call_args = self.client.entity_api.search_for_entities.call_args_list[3]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XNYS", "ticker": "M"},
            kwargs,
            "Arguments not as expected",
        )

        # fifth call - entity = "entityType/company" ticker = "001" / market = "XHKG"
        call_args = self.client.entity_api.search_for_entities.call_args_list[4]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "mic": "XHKG", "ticker": "001"},
            kwargs,
            "Arguments not as expected",
        )

    def test_create_mapping_isin(self):

        args = [
            "script-name",
            "--filename-input",
            "./exabel_data_sdk/tests/resources/data/mapping_isin.csv",
            "--filename-output",
            self.temp_file.name,
            "--api-key",
            "123",
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTestISIN")
        script.run_script(self.client, script.parse_arguments())

        # first call - entity = "entityType/company" isin = 'NO12345678'
        call_args = self.client.entity_api.search_for_entities.call_args_list[0]
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
            "./exabel_data_sdk/tests/resources/data/mapping_factset_identifier.csv",
            "--filename-output",
            self.temp_file.name,
            "--api-key",
            "123",
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTestISIN")
        script.run_script(self.client, script.parse_arguments())

        # first call - entity = "entityType/company" factset_identifier = '0MXNWD-E'
        call_args = self.client.entity_api.search_for_entities.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "factset_identifier": "0MXNWD-E"},
            kwargs,
            "Arguments not as expected",
        )

        # second call - entity = "entityType/company" factset_identifier = 'DT699H-S'
        call_args = self.client.entity_api.search_for_entities.call_args_list[1]
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
            "./exabel_data_sdk/tests/resources/data/mapping_bloomberg_ticker.csv",
            "--filename-output",
            self.temp_file.name,
            "--api-key",
            "123",
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTestISIN")
        script.run_script(self.client, script.parse_arguments())

        # first call - entity = "entityType/company" bloomberg_ticker = 'AAPL US'
        call_args = self.client.entity_api.search_for_entities.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "bloomberg_ticker": "AAPL US"},
            kwargs,
            "Arguments not as expected",
        )

        # second call - entity = "entityType/company" bloomberg_ticker = 'AMZN US'
        call_args = self.client.entity_api.search_for_entities.call_args_list[1]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "bloomberg_ticker": "AMZN US"},
            kwargs,
            "Arguments not as expected",
        )

    def test_create_mapping_figi(self):

        args = [
            "script-name",
            "--filename-input",
            "./exabel_data_sdk/tests/resources/data/mapping_figi.csv",
            "--filename-output",
            self.temp_file.name,
            "--api-key",
            "123",
        ]

        script = CreateEntityMappingFromCsv(args, "MappingTestFIGI")
        script.run_script(self.client, script.parse_arguments())

        # first call - entity = "entityType/company" figi = 'BBG000B9Y5X2'
        call_args = self.client.entity_api.search_for_entities.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "figi": "BBG000B9Y5X2"},
            kwargs,
            "Arguments not as expected",
        )

        # second call - entity = "entityType/company" figi = 'BBG001S5N8V8'
        call_args = self.client.entity_api.search_for_entities.call_args_list[1]
        _, kwargs = call_args
        self.assertEqual(
            {"entity_type": "entityTypes/company", "figi": "BBG001S5N8V8"},
            kwargs,
            "Arguments not as expected",
        )


if __name__ == "__main__":
    unittest.main()
