import unittest

from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.scripts.load_relationships_from_csv import LoadRelationshipsFromCsv
from exabel_data_sdk.tests.scripts.common_utils import load_test_data_from_csv

common_args = [
    "script-name",
    "--namespace",
    "acme",
    "--api-key",
    "123",
    "--relationship_type",
    "PART_OF",
    "--entity_to_column",
    "brand",
]


class TestLoadRelationships(unittest.TestCase):
    def test_read_file(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/relationships.csv",
            "--entity_from_column",
            "entity_from",
            "--description_column",
            "description",
        ]
        client = load_test_data_from_csv(LoadRelationshipsFromCsv, args)
        # Check that the relationship type was created
        self.assertEqual(
            RelationshipType("relationshipTypes/acme.PART_OF"),
            client.relationship_api.get_relationship_type("relationshipTypes/acme.PART_OF"),
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
            "--entity_from_column",
            "company",
        ]
        client = load_test_data_from_csv(LoadRelationshipsFromCsv, args)
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
        all_relationships = client.relationship_api.list_relationships().results
        self.assertListEqual(expected_relationships, all_relationships)
        for expected_relationship in expected_relationships:
            relationship = client.relationship_api.get_relationship(
                expected_relationship.relationship_type,
                expected_relationship.from_entity,
                expected_relationship.to_entity,
            )
            self.assertEqual(expected_relationship, relationship)
