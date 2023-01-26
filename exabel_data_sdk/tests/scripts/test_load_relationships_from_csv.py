import unittest
from unittest.mock import MagicMock, patch

from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.scripts.load_relationships_from_csv import LoadRelationshipsFromCsv
from exabel_data_sdk.tests.scripts.common_utils import load_test_data_from_csv

common_args = [
    "script-name",
    "--api-key",
    "123",
    "--relationship-type",
    "PART_OF",
]
common_args_with_entity_to_column = common_args + [
    "--entity-to-column",
    "BRAND",
]


class TestLoadRelationships(unittest.TestCase):
    def test_read_file(self):
        args = common_args_with_entity_to_column + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/relationships.csv",
            "--entity-from-column",
            "entity_from",
            "--description-column",
            "description",
        ]
        client = load_test_data_from_csv(LoadRelationshipsFromCsv, args, namespace="acme")
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/acme.PART_OF",
                from_entity="entityTypes/company/company_x",
                to_entity="entityTypes/brand/entities/acme.Spring_Vine",
                description="Owned since 2019",
            ),
            Relationship(
                relationship_type="relationshipTypes/acme.PART_OF",
                from_entity="entityTypes/company/company_y",
                to_entity="entityTypes/brand/entities/acme.The_Coconut_Tree",
                description="Acquired for $200M",
            ),
        ]
        self.check_relationships(client, expected_relationships)

    def test_read_file_opposite_from_to_relationship(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/relationships.csv",
            "--entity-from-column",
            "BRAND",
            "--entity-to-column",
            "entity_from",
            "--description-column",
            "description",
        ]
        client = load_test_data_from_csv(LoadRelationshipsFromCsv, args, namespace="acme")
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/acme.PART_OF",
                from_entity="entityTypes/brand/entities/acme.Spring_Vine",
                to_entity="entityTypes/company/company_x",
                description="Owned since 2019",
            ),
            Relationship(
                relationship_type="relationshipTypes/acme.PART_OF",
                from_entity="entityTypes/brand/entities/acme.The_Coconut_Tree",
                to_entity="entityTypes/company/company_y",
                description="Acquired for $200M",
            ),
        ]
        self.check_relationships(client, expected_relationships)

    def test_read_file_with_default_entity_from_to_columns(self):
        args_default_from_to_columns = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/relationships.csv",
            "--description-column",
            "description",
        ]
        client = load_test_data_from_csv(
            LoadRelationshipsFromCsv, args_default_from_to_columns, namespace="acme"
        )
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/acme.PART_OF",
                from_entity="entityTypes/company/company_x",
                to_entity="entityTypes/brand/entities/acme.Spring_Vine",
                description="Owned since 2019",
            ),
            Relationship(
                relationship_type="relationshipTypes/acme.PART_OF",
                from_entity="entityTypes/company/company_y",
                to_entity="entityTypes/brand/entities/acme.The_Coconut_Tree",
                description="Acquired for $200M",
            ),
        ]
        self.check_relationships(client, expected_relationships)

    def test_read_file_with_integer_identifiers(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/relationships_with_integer_identifiers.csv",
            "--entity-from-column",
            "company",
            "--entity-to-column",
            "brand",
        ]
        client = load_test_data_from_csv(LoadRelationshipsFromCsv, args, namespace="acme")
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/acme.PART_OF",
                from_entity="entityTypes/company/entities/acme.0010",
                to_entity="entityTypes/brand/entities/acme.0001",
            ),
            Relationship(
                relationship_type="relationshipTypes/acme.PART_OF",
                from_entity="entityTypes/company/entities/acme.0011",
                to_entity="entityTypes/brand/entities/acme.0002",
            ),
        ]
        self.check_relationships(client, expected_relationships)

    def check_relationships(self, client, expected_relationships):
        """Check expected entities against actual entities retrieved from the client"""
        relationship_type = expected_relationships[0].relationship_type
        all_relationships = client.relationship_api.list_relationships(relationship_type)
        self.assertCountEqual(expected_relationships, all_relationships)
        for expected_relationship in expected_relationships:
            relationship = client.relationship_api.get_relationship(
                expected_relationship.relationship_type,
                expected_relationship.from_entity,
                expected_relationship.to_entity,
            )
            self.assertEqual(expected_relationship, relationship)

    def test_read_file_with_upsert(self):
        args = common_args_with_entity_to_column + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/relationships.csv",
            "--entity-from-column",
            "entity_from",
            "--description-column",
            "DESCRIPTION",
            "--upsert",
        ]
        client = load_test_data_from_csv(LoadRelationshipsFromCsv, args, namespace="acme")
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/acme.PART_OF",
                from_entity="entityTypes/company/company_x",
                to_entity="entityTypes/brand/entities/acme.Spring_Vine",
                description="This entry might be ignored because it's a duplicate",
            ),
            Relationship(
                relationship_type="relationshipTypes/acme.PART_OF",
                from_entity="entityTypes/company/company_y",
                to_entity="entityTypes/brand/entities/acme.The_Coconut_Tree",
                description="Acquired for $200M",
            ),
        ]
        self.check_relationships(client, expected_relationships)
        client = load_test_data_from_csv(LoadRelationshipsFromCsv, args, client)
        self.check_relationships(client, expected_relationships)

    @patch("exabel_data_sdk.scripts.load_relationships_from_csv.parse_property_columns")
    def test_property_columns(self, mock_parser):
        args = common_args + [
            "--filename",
            "the-filename",
            "--entity-from-column",
            "the-entity-from-column",
            "--entity-to-column",
            "the-entity-to-column",
            "--property-columns",
            "THE-PROPERTY-COLUMN",
            "THE-OTHER-PROPERTY-COLUMN",
        ]
        client = MagicMock()
        with patch("exabel_data_sdk.scripts.load_relationships_from_csv.CsvRelationshipLoader"):
            csv_loader = LoadRelationshipsFromCsv(args, "the-description")
            parsed_args = csv_loader.parse_arguments()
            csv_loader.run_script(client, parsed_args)
        mock_parser.assert_called_once_with("the-property-column", "the-other-property-column")
