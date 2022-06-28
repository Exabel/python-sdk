import unittest

from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.exabel_client import ExabelClient
from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.csv_relationship_loader import CsvRelationshipLoader
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient


class TestCsvRelationshipLoader(unittest.TestCase):
    def test_load_relationships_with_properties(self):
        client: ExabelClient = ExabelMockClient()
        CsvRelationshipLoader(client).load_relationships(
            filename="exabel_data_sdk/tests/resources/data/relationships_with_properties.csv",
            namespace="test",
            relationship_type="HAS_BRAND",
            entity_from_column="company",
            entity_to_column="brand",
            property_columns={
                "boolean_prop": bool,
                "string_prop": str,
                "integer_prop": int,
                "float_prop": float,
            },
            upsert=False,
        )

        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/entities/test.1",
                to_entity="entityTypes/brand/entities/test.1",
                description="",
                properties={
                    "boolean_prop": True,
                    "string_prop": "string",
                    "integer_prop": 1,
                    "float_prop": 1.0,
                },
                read_only=False,
            ),
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/entities/test.1",
                to_entity="entityTypes/brand/entities/test.2",
                description="",
                properties={
                    "boolean_prop": True,
                    "string_prop": "STRING",
                    "integer_prop": 2,
                    "float_prop": 2.3,
                },
                read_only=False,
            ),
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/entities/test.1",
                to_entity="entityTypes/brand/entities/test.3",
                description="",
                properties={
                    "boolean_prop": False,
                    "string_prop": "string",
                    "integer_prop": 3,
                    "float_prop": 3.0,
                },
                read_only=False,
            ),
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/entities/test.1",
                to_entity="entityTypes/brand/entities/test.4",
                description="",
                properties={},
                read_only=False,
            ),
        ]
        actual_relationships = client.relationship_api.list_relationships().results
        self.assertCountEqual(expected_relationships, actual_relationships)

    def test_load_relationships_with_non_existent_property(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(CsvLoadingException):
            CsvRelationshipLoader(client).load_relationships(
                filename="exabel_data_sdk/tests/resources/data/relationships_with_properties.csv",
                namespace="test",
                relationship_type="HAS_BRAND",
                entity_from_column="company",
                entity_to_column="brand",
                property_columns={"non_existent_prop": str},
                upsert=False,
            )

    def test_load_relationships_with_non_existent_relationship_type(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(CsvLoadingException):
            CsvRelationshipLoader(client).load_relationships(
                filename="exabel_data_sdk/tests/resources/data/relationships.csv",
                namespace="test",
                relationship_type="NON_EXISTENT_RELATIONSHIPTYPE",
                entity_from_column="entity_from",
                entity_to_column="brand",
                upsert=False,
            )

    def test_load_relationships_with_existent_relationship_type(self):
        client: ExabelClient = ExabelMockClient()
        CsvRelationshipLoader(client).load_relationships(
            filename="exabel_data_sdk/tests/resources/data/relationships.csv",
            namespace="test",
            relationship_type="HAS_BRAND",
            entity_from_column="entity_from",
            entity_to_column="brand",
            upsert=False,
        )
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/company_x",
                to_entity="entityTypes/brand/entities/test.Spring_Vine",
                read_only=False,
            ),
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/company_y",
                to_entity="entityTypes/brand/entities/test.The_Coconut_Tree",
                read_only=False,
            ),
        ]
        actual_relationships = client.relationship_api.list_relationships().results
        self.assertCountEqual(expected_relationships, actual_relationships)

    def test_load_relationships_only_entity_from_column_specified(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(CsvLoadingException) as exception_context:
            CsvRelationshipLoader(client).load_relationships(
                filename="exabel_data_sdk/tests/resources/data/relationships.csv",
                namespace="test",
                relationship_type="NON_EXISTENT_RELATIONSHIPTYPE",
                entity_from_column="entity_from",
                upsert=False,
            )
        self.assertEqual(
            "Both entity_from_column and entity_to_column must be None, or both must be set. "
            "Got: entity_from_column=entity_from, entity_to_column=None",
            str(exception_context.exception),
        )

    def test_load_relationships_only_entity_to_column_specified(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(CsvLoadingException) as exception_context:
            CsvRelationshipLoader(client).load_relationships(
                filename="exabel_data_sdk/tests/resources/data/relationships.csv",
                namespace="test",
                relationship_type="NON_EXISTENT_RELATIONSHIPTYPE",
                entity_to_column="brand",
                upsert=False,
            )
        self.assertEqual(
            "Both entity_from_column and entity_to_column must be None, or both must be set. "
            "Got: entity_from_column=None, entity_to_column=brand",
            str(exception_context.exception),
        )

    def test_load_relationships_default_entity_from_to_columns(self):
        client: ExabelClient = ExabelMockClient()
        CsvRelationshipLoader(client).load_relationships(
            filename="exabel_data_sdk/tests/resources/data/relationships_with_properties.csv",
            namespace="test",
            relationship_type="HAS_BRAND",
            upsert=False,
        )
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/entities/test.1",
                to_entity="entityTypes/brand/entities/test.1",
                read_only=False,
            ),
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/entities/test.1",
                to_entity="entityTypes/brand/entities/test.2",
                read_only=False,
            ),
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/entities/test.1",
                to_entity="entityTypes/brand/entities/test.3",
                read_only=False,
            ),
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/entities/test.1",
                to_entity="entityTypes/brand/entities/test.4",
                read_only=False,
            ),
        ]
        actual_relationships = client.relationship_api.list_relationships().results
        self.assertCountEqual(expected_relationships, actual_relationships)
