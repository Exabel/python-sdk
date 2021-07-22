import unittest
from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.service.import_service import CsvImportService


class TestCreateEntitiesFromCsv(unittest.TestCase):
    def test_create_entities_with_description(self):

        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.entity_api.entity_exists.return_value = False
        service = CsvImportService(client)
        result = service.create_entities_from_csv(
            filename_input="./tests/resources/data/entities_with_description.csv", separator=";")

        # first row
        # entityTypes/brand/test.brand_y;brand_y;brand_y description
        # fails with ValueError
        self.assertEqual(result["entityTypes/brand/test.brand_y"], None, "Result not as expected")

        # second row
        # entityTypes/brand/entities/test.BRAND_X;BRAND_X;BRAND_X description
        call_args = client.entity_api.create_entity.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {
                "entity": Entity(
                    name="entityTypes/brand/entities/test.BRAND_X",
                    display_name="BRAND_X",
                    description="BRAND_X description",
                    properties={},
                ),
                "entity_type": "entityTypes/brand",
            },
            kwargs,
            "Arguments not as expected",
        )
        self.assertNotEqual(
            result["entityTypes/brand/entities/test.BRAND_X"], None, "Result not as expected"
        )

    def test_create_entities_with_existing_entity(self):

        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.entity_api.entity_exists.return_value = True
        service = CsvImportService(client)
        result = service.create_entities_from_csv(
            filename_input="./tests/resources/data/entities_with_description.csv", separator=";")

        # first row
        # entityTypes/brand/test.brand_y;brand_y;brand_y description
        # fails with ValueError
        self.assertEqual(result["entityTypes/brand/test.brand_y"], None, "Result not as expected")

        # second row
        # entityTypes/brand/entities/test.BRAND_X;BRAND_X;BRAND_X description
        self.assertEqual(client.entity_api.create_entity.call_args_list, [], "Unexpected call")
        self.assertTrue(
            "entityTypes/brand/entities/test.BRAND_X" not in result, "Result not as expected"
        )

    def test_create_entities_without_description(self):
        args = [
            "script-name",
            "--filename-input",
            "./tests/resources/data/entities_without_description.csv",
        ]

        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.entity_api.entity_exists.return_value = False
        service = CsvImportService(client)
        result = service.create_entities_from_csv(
            filename_input="./tests/resources/data/entities_without_description.csv", separator=";")

        # first row
        # entityTypes/brand/entities/test.BRAND_X;BRAND_X
        call_args = client.entity_api.create_entity.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {
                "entity": Entity(
                    name="entityTypes/brand/entities/test.BRAND_X",
                    display_name="BRAND_X",
                    description="",
                    properties={},
                ),
                "entity_type": "entityTypes/brand",
            },
            kwargs,
            "Arguments not as expected",
        )
        self.assertNotEqual(
            result["entityTypes/brand/entities/test.BRAND_X"], None, "Result not as expected"
        )


if __name__ == "__main__":
    unittest.main()
