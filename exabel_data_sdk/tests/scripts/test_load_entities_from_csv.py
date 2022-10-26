import random
import unittest
from unittest.mock import MagicMock, patch

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.scripts.load_entities_from_csv import LoadEntitiesFromCsv
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient
from exabel_data_sdk.tests.scripts.common_utils import load_test_data_from_csv

common_args = [
    "script-name",
    "--namespace",
    "test",
    "--api-key",
    "123",
]


class TestLoadEntities(unittest.TestCase):
    def test_read_file_with_uppercased_entity_type_in_column_non_existing(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities.csv",
            "--name-column",
            "brand",
            "--display-name-column",
            "brand",
            "--description-column",
            "description",
        ]
        client = load_test_data_from_csv(LoadEntitiesFromCsv, args)
        expected_entities = [
            Entity(
                name="entityTypes/brand/entities/test.Spring_Vine",
                display_name="Spring & Vine",
                description="Shampoo bars",
            ),
            Entity(
                name="entityTypes/brand/entities/test.The_Coconut_Tree",
                display_name="The Coconut Tree",
                description="Sri Lankan street food",
            ),
        ]
        self.check_entities(client, expected_entities)

    def test_read_file__non_existent_entity_column_should_fail(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities.csv",
            "--description-column",
            "description",
            "--name-column",
            "COMPANY",
        ]
        with self.assertRaises(KeyError) as context:
            load_test_data_from_csv(LoadEntitiesFromCsv, args)
        self.assertEqual("company", context.exception.args[0])

    def test_read_file_with_uppercased_entity_type_in_argument_existing(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities.csv",
            "--description-column",
            "description",
            "--entity-type",
            "ANOTHER_BRAND",
            "--name-column",
            "BRAND",
            "--display-name-column",
            "BRAND",
        ]
        script = LoadEntitiesFromCsv(args, f"Test{type(LoadEntitiesFromCsv).__name__}")
        client = ExabelMockClient()
        client.entity_api.create_entity_type(
            EntityType(
                name="entityTypes/ANOTHER_BRAND",
                display_name="Another Brand Uppercased",
                description="This is another uppercased brand",
            )
        )
        script.run_script(client, script.parse_arguments())

        expected_entities = [
            Entity(
                name="entityTypes/ANOTHER_BRAND/entities/test.Spring_Vine",
                display_name="Spring & Vine",
                description="Shampoo bars",
            ),
            Entity(
                name="entityTypes/ANOTHER_BRAND/entities/test.The_Coconut_Tree",
                display_name="The Coconut Tree",
                description="Sri Lankan street food",
            ),
        ]
        self.check_entities(
            client, expected_entities, expected_entity_type="entityTypes/ANOTHER_BRAND"
        )

    def test_read_file_with_integer_identifier(self):
        file_args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities_with_integer_identifiers.csv",
        ]
        extra_args = [[], ["--name-column", "brand"]]
        expected_entities = [
            Entity(name="entityTypes/brand/entities/test.0001", display_name="Spring & Vine"),
            Entity(name="entityTypes/brand/entities/test.0002", display_name="The Coconut Tree"),
        ]
        for e_args in extra_args:
            args = file_args + e_args
            client = load_test_data_from_csv(LoadEntitiesFromCsv, args)
            self.check_entities(client, expected_entities)

    def check_entities(
        self, client, expected_entities, expected_entity_type: str = "entityTypes/brand"
    ):
        """Check expected entities against actual entities retrieved from the client"""
        all_entities = client.entity_api.list_entities(expected_entity_type).results
        self.assertListEqual(sorted(expected_entities), sorted(all_entities))
        for expected_entity in expected_entities:
            entity = client.entity_api.get_entity(expected_entity.name)
            self.assertEqual(expected_entity, entity)

    def test_read_file_with_duplicated_entity_identifiers_should_fail(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities_with_duplicated_brands.csv",
            "--description-column",
            "description",
        ]
        with self.assertRaises(ValueError) as context:
            load_test_data_from_csv(LoadEntitiesFromCsv, args)
        self.assertEqual(
            "Duplicate entities in "
            "./exabel_data_sdk/tests/resources/data/entities_with_duplicated_brands.csv",
            str(context.exception),
        )

    def test_read_file_random_errors(self):
        random.seed(1)
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities2.csv",
        ]
        client = load_test_data_from_csv(LoadEntitiesFromCsv, args)
        client.entity_api.entities.failure_rate = 0.3
        expected_entities = [
            Entity(
                name=f"entityTypes/brand/entities/test.Brand_{letter}",
                display_name=f"Brand {letter}",
            )
            for letter in "ABCDEFGHIJ"
        ]
        self.check_entities(client, expected_entities)

    def test_read_file_with_upsert(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities.csv",
            "--display-name-column",
            "brand",
            "--description-column",
            "description",
            "--upsert",
        ]
        client = load_test_data_from_csv(LoadEntitiesFromCsv, args)
        expected_entities = [
            Entity(
                name="entityTypes/brand/entities/test.Spring_Vine",
                display_name="Spring & Vine",
                description="Shampoo bars",
            ),
            Entity(
                name="entityTypes/brand/entities/test.The_Coconut_Tree",
                display_name="The Coconut Tree",
                description="Sri Lankan street food",
            ),
        ]
        self.check_entities(client, expected_entities)
        client = load_test_data_from_csv(LoadEntitiesFromCsv, args, client)
        self.check_entities(client, expected_entities)

    @patch("exabel_data_sdk.scripts.load_entities_from_csv.parse_property_columns")
    def test_property_columns(self, mock_parser):
        args = common_args + [
            "--filename",
            "the-filename",
            "--property-columns",
            "the-property-column",
            "the-other-property-column",
        ]
        client = MagicMock()
        with patch("exabel_data_sdk.scripts.load_entities_from_csv.CsvEntityLoader"):
            csv_loader = LoadEntitiesFromCsv(args, "the-description")
            parsed_args = csv_loader.parse_arguments()
            csv_loader.run_script(client, parsed_args)
        mock_parser.assert_called_once_with("the-property-column", "the-other-property-column")
