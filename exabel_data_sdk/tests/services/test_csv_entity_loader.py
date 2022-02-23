import unittest

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.exabel_client import ExabelClient
from exabel_data_sdk.services.csv_entity_loader import CsvEntityLoader
from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient


class TestCsvEntityLoader(unittest.TestCase):
    def test_load_entities_with_properties(self):
        client: ExabelClient = ExabelMockClient()
        CsvEntityLoader(client).load_entities(
            filename="exabel_data_sdk/tests/resources/data/entities_with_properties.csv",
            namespace="test",
            name_column="brand",
            property_columns={
                "boolean_prop": bool,
                "string_prop": str,
                "integer_prop": int,
                "float_prop": float,
            },
            upsert=False,
        )

        expected_entities = [
            Entity(
                name="entityTypes/brand/entities/test.1",
                display_name="1",
                description="",
                properties={
                    "boolean_prop": True,
                    "string_prop": "string",
                    "integer_prop": 1,
                    "float_prop": 1.0,
                },
                read_only=False,
            ),
            Entity(
                name="entityTypes/brand/entities/test.2",
                display_name="2",
                description="",
                properties={
                    "boolean_prop": True,
                    "string_prop": "STRING",
                    "integer_prop": 2,
                    "float_prop": 2.3,
                },
                read_only=False,
            ),
            Entity(
                name="entityTypes/brand/entities/test.3",
                display_name="3",
                description="",
                properties={
                    "boolean_prop": False,
                    "string_prop": "string",
                    "integer_prop": 3,
                    "float_prop": 3.0,
                },
                read_only=False,
            ),
            Entity(
                name="entityTypes/brand/entities/test.4",
                display_name="4",
                description="",
                properties={},
                read_only=False,
            ),
        ]
        actual_entities = client.entity_api.list_entities("entityTypes/brand").results
        self.assertSequenceEqual(expected_entities, actual_entities)

    def test_load_entities_with_non_existent_property(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(CsvLoadingException):
            CsvEntityLoader(client).load_entities(
                filename="exabel_data_sdk/tests/resources/data/entities_with_properties.csv",
                namespace="test",
                name_column="brand",
                property_columns={"non_existent_prop": str},
                upsert=False,
            )
