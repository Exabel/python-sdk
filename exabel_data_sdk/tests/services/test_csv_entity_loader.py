import unittest
from unittest import mock

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.exabel_client import ExabelClient
from exabel_data_sdk.services.csv_entity_loader import CsvEntityLoader
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient


class TestCsvEntityLoader(unittest.TestCase):
    def test_load_entities_with_properties(self):
        client: ExabelClient = ExabelMockClient()
        CsvEntityLoader(client).load_entities(
            filename="exabel_data_sdk/tests/resources/data/entities_with_properties.csv",
            namespace="test",
            entity_column="brand",
            display_name_column="brand",
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

    def test_load_entities_with_integer_display_names(self):
        client: ExabelClient = ExabelMockClient()
        CsvEntityLoader(client).load_entities(
            filename="exabel_data_sdk/tests/resources/data/entities_with_integer_display_names.csv",
            entity_type="brand",
            upsert=False,
        )

        expected_entities = [
            Entity(
                name="entityTypes/brand/entities/test.0001",
                display_name="0001",
            ),
            Entity(
                name="entityTypes/brand/entities/test.0002",
                display_name="0002",
            ),
        ]
        actual_entities = client.entity_api.list_entities("entityTypes/brand").results
        self.assertSequenceEqual(expected_entities, actual_entities)

    def test_load_entities_with_non_existent_property(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException):
            CsvEntityLoader(client).load_entities(
                filename="exabel_data_sdk/tests/resources/data/entities_with_properties.csv",
                namespace="test",
                entity_column="brand",
                property_columns={"non_existent_prop": str},
                upsert=False,
            )

    def test_load_entities_with_uppercase_columns(self):
        client: ExabelClient = ExabelMockClient()
        CsvEntityLoader(client).load_entities(
            filename="exabel_data_sdk/tests/resources/data/entities_with_uppercase_columns.csv",
            namespace="test",
            entity_column="brand",
            display_name_column="display_name",
            description_column="description",
            property_columns={
                "prop": bool,
            },
            upsert=False,
        )

        expected_entities = [
            Entity(
                name="entityTypes/brand/entities/test.1",
                display_name="One",
                description="This is One",
                properties={
                    "prop": True,
                },
                read_only=False,
            ),
            Entity(
                name="entityTypes/brand/entities/test.2",
                display_name="Two",
                description="This is Two",
                properties={
                    "prop": True,
                },
                read_only=False,
            ),
            Entity(
                name="entityTypes/brand/entities/test.3",
                display_name="Three",
                description="This is Three",
                properties={
                    "prop": False,
                },
                read_only=False,
            ),
            Entity(
                name="entityTypes/brand/entities/test.4",
                display_name="",
                description="",
                properties={},
                read_only=False,
            ),
        ]
        self.maxDiff = 2000
        actual_entities = client.entity_api.list_entities("entityTypes/brand").results
        self.assertSequenceEqual(expected_entities, actual_entities)

    @mock.patch("exabel_data_sdk.services.csv_reader.CsvReader.read_file")
    def test_load_entities__display_name_with_only_one_column(self, mock_read_file):
        mock_read_file.return_value = pd.DataFrame([{"brand": "brand1"}])
        client: ExabelClient = ExabelMockClient()
        CsvEntityLoader(client).load_entities(
            filename="filename",
            namespace="test",
            upsert=False,
        )
        self.assertCountEqual(
            [Entity(name="entityTypes/brand/entities/test.brand1", display_name="brand1")],
            client.entity_api.list_entities("entityTypes/brand").results,
        )

    @mock.patch("exabel_data_sdk.services.csv_reader.CsvReader.read_file")
    def test_load_entities__with_batch_size(self, mock_read_file: mock.MagicMock):
        df = pd.DataFrame([{"brand": "brand"}])
        mock_read_file.side_effect = [df, (df for _ in range(2))]
        client = mock.create_autospec(ExabelClient)
        loader = CsvEntityLoader(client)
        with mock.patch.object(loader, "_load_entities") as mock_load:
            loader.load_entities(
                filename="file",
                batch_size=1,
            )
        self.assertIsNone(mock_read_file.call_args_list[0][1].get("chunksize"))
        self.assertEqual(mock_read_file.call_args_list[1][1]["chunksize"], 1)
        self.assertEqual(mock_load.call_count, 2)
