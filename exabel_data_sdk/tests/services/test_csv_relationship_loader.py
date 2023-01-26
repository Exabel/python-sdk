import unittest
from typing import Sequence
from unittest import mock

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.api.relationship_api import RelationshipApi
from exabel_data_sdk.client.api.search_service import SearchService
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.client.exabel_client import ExabelClient
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
)
from exabel_data_sdk.services.csv_loading_result import CsvLoadingResult
from exabel_data_sdk.services.csv_relationship_loader import (
    CsvRelationshipLoader,
    RelationshipLoaderColumnConfiguration,
)
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.services.file_loading_result import FileLoadingResult
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import SearchEntitiesResponse, SearchTerm
from exabel_data_sdk.stubs.exabel.api.data.v1.entity_messages_pb2 import Entity
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient

# pylint: disable=protected-access


class TestRelationshipLoaderColumnConfiguration(unittest.TestCase):
    def test_validate_argument_combination(self):
        RelationshipLoaderColumnConfiguration._validate_argument_combination()
        RelationshipLoaderColumnConfiguration._validate_argument_combination(
            from_entity_column="from_entity_column", to_entity_column="to_entity_column"
        )
        RelationshipLoaderColumnConfiguration._validate_argument_combination(
            from_entity_type="from_entity_type",
            from_entity_column="from_entity_column",
            to_entity_type="to_entity_type",
            to_entity_column="to_entity_column",
        )
        RelationshipLoaderColumnConfiguration._validate_argument_combination(
            from_entity_type="from_entity_type",
            to_entity_type="to_entity_type",
        )
        RelationshipLoaderColumnConfiguration._validate_argument_combination(
            from_entity_type="company",
            from_entity_column="from_entity_column",
            from_identifier_type="from_identifier_type",
            to_entity_type="to_entity_type",
            to_entity_column="to_entity_column",
        )
        RelationshipLoaderColumnConfiguration._validate_argument_combination(
            from_entity_type="from_entity_type",
            from_entity_column="from_entity_column",
            to_entity_type="company",
            to_entity_column="to_entity_column",
            to_identifier_type="to_identifier_type",
        )

    def test_validate_argument_combination__invalid_combinations(self):
        with self.assertRaises(ValueError):
            RelationshipLoaderColumnConfiguration._validate_argument_combination(
                from_entity_type="from_entity_type"
            )
        with self.assertRaises(ValueError):
            RelationshipLoaderColumnConfiguration._validate_argument_combination(
                to_entity_type="to_entity_type"
            )
        with self.assertRaises(ValueError):
            RelationshipLoaderColumnConfiguration._validate_argument_combination(
                from_entity_column="from_entity_column"
            )
        with self.assertRaises(ValueError):
            RelationshipLoaderColumnConfiguration._validate_argument_combination(
                to_entity_column="to_entity_column"
            )
        with self.assertRaises(ValueError):
            RelationshipLoaderColumnConfiguration._validate_argument_combination(
                from_identifier_type="from_identifier_type",
            )
        with self.assertRaises(ValueError):
            RelationshipLoaderColumnConfiguration._validate_argument_combination(
                to_identifier_type="to_identifier_type",
            )
        with self.assertRaises(ValueError):
            RelationshipLoaderColumnConfiguration._validate_argument_combination(
                from_entity_type="not_company",
                from_identifier_type="from_identifier_type",
                to_entity_type="to_entity_type",
            )
        with self.assertRaises(ValueError):
            RelationshipLoaderColumnConfiguration._validate_argument_combination(
                from_entity_type="from_entity_type",
                to_entity_type="not_company",
                to_identifier_type="to_identifier_type",
            )

    def test_from_default_values(self):
        config = RelationshipLoaderColumnConfiguration._from_default_values()
        self.assertIsNone(config.from_column.entity_type)
        self.assertEqual(0, config.from_column.index)
        self.assertIsNone(config.to_column.entity_type)
        self.assertEqual(1, config.to_column.index)

    def test_from_entity_types(self):
        config = RelationshipLoaderColumnConfiguration._from_entity_types(
            from_entity_type="from_entity_type", to_entity_type="to_entity_type"
        )
        self.assertEqual("from_entity_type", config.from_column.entity_type)
        self.assertEqual(0, config.from_column.index)
        self.assertEqual("to_entity_type", config.to_column.entity_type)
        self.assertEqual(1, config.to_column.index)

    def test_from_entity_types__with_entity_columns(self):
        config = RelationshipLoaderColumnConfiguration._from_entity_types(
            from_entity_type="from_entity_type",
            to_entity_type="to_entity_type",
            from_entity_column="from_entity_column",
            to_entity_column="to_entity_column",
        )
        self.assertEqual("from_entity_type", config.from_column.entity_type)
        self.assertEqual("from_entity_column", config.from_column.name)
        self.assertEqual("to_entity_type", config.to_column.entity_type)
        self.assertEqual("to_entity_column", config.to_column.name)

    def test_from_entity_types__with_identifiers(self):
        config = RelationshipLoaderColumnConfiguration._from_entity_types(
            from_entity_type="company",
            from_identifier_type="from_identifier_type",
            to_entity_type="company",
            to_identifier_type="to_identifier_type",
        )
        self.assertEqual("from_identifier_type", config.from_column.entity_type)
        self.assertEqual(0, config.from_column.index)
        self.assertEqual("to_identifier_type", config.to_column.entity_type)
        self.assertEqual(1, config.to_column.index)

    def test_from_specified_columns(self):
        config = RelationshipLoaderColumnConfiguration._from_specified_columns(
            from_entity_column="from_entity_column", to_entity_column="to_entity_column"
        )
        self.assertIsNone(config.from_column.entity_type)
        self.assertEqual("from_entity_column", config.from_column.name)
        self.assertIsNone(config.to_column.entity_type)
        self.assertEqual("to_entity_column", config.to_column.name)

    def test_from_arguments(self):
        config = RelationshipLoaderColumnConfiguration.from_arguments(
            from_entity_type="company",
            from_entity_column="from_entity_column",
            from_identifier_type="from_identifier_type",
            to_entity_type="company",
            to_entity_column="to_entity_column",
            to_identifier_type="to_identifier_type",
        )
        self.assertEqual("from_identifier_type", config.from_column.entity_type)
        self.assertEqual("from_entity_column", config.from_column.name)
        self.assertEqual("to_identifier_type", config.to_column.entity_type)
        self.assertEqual("to_entity_column", config.to_column.name)


class TestCsvRelationshipLoader(unittest.TestCase):
    def test_load_relationships_with_properties(self):
        client: ExabelClient = ExabelMockClient()
        CsvRelationshipLoader(client).load_relationships(
            filename="exabel_data_sdk/tests/resources/data/relationships_with_properties.csv",
            relationship_type="HAS_BRAND",
            from_entity_column="company",
            to_entity_column="brand",
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
        actual_relationships = client.relationship_api.list_relationships(
            "relationshipTypes/test.HAS_BRAND"
        )
        self.assertCountEqual(expected_relationships, actual_relationships)

    def test_load_relationships_with_non_existent_property(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException):
            CsvRelationshipLoader(client).load_relationships(
                filename="exabel_data_sdk/tests/resources/data/relationships_with_properties.csv",
                relationship_type="HAS_BRAND",
                from_entity_column="company",
                to_entity_column="brand",
                property_columns={"non_existent_prop": str},
                upsert=False,
            )

    def test_load_relationships_with_non_existent_relationship_type(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException):
            CsvRelationshipLoader(client).load_relationships(
                filename="exabel_data_sdk/tests/resources/data/relationships.csv",
                relationship_type="NON_EXISTENT_RELATIONSHIPTYPE",
                from_entity_column="entity_from",
                to_entity_column="brand",
                upsert=False,
            )

    def test_load_relationships_with_existent_relationship_type_existent_uppercase_entity_type(
        self,
    ):
        client: ExabelClient = ExabelMockClient()
        client.entity_api = mock.create_autospec(EntityApi(ClientConfig(api_key="123")))
        client.entity_api.get_entity_type_iterator.side_effect = self._list_entity_types
        result = CsvRelationshipLoader(client).load_relationships(
            filename="exabel_data_sdk/tests/resources/data/relationships.csv",
            relationship_type="HAS_BRAND",
            entity_from_column="entity_from",
            entity_to_column="brand",
            upsert=False,
        )
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/company_x",
                to_entity="entityTypes/BRAND/entities/test.Spring_Vine",
                read_only=False,
            ),
            Relationship(
                relationship_type="relationshipTypes/test.HAS_BRAND",
                from_entity="entityTypes/company/company_y",
                to_entity="entityTypes/BRAND/entities/test.The_Coconut_Tree",
                read_only=False,
            ),
        ]
        actual_relationships = client.relationship_api.list_relationships(
            "relationshipTypes/test.HAS_BRAND"
        )
        self.assertCountEqual(expected_relationships, actual_relationships)
        self.assertIsInstance(result, FileLoadingResult)
        self.assertIsInstance(result, CsvLoadingResult)

    def test_load_relationships_with_existent_relationship_type_non_existent_uppercase_entity_type(
        self,
    ):
        client: ExabelClient = ExabelMockClient()
        result = CsvRelationshipLoader(client).load_relationships(
            filename="exabel_data_sdk/tests/resources/data/relationships.csv",
            relationship_type="HAS_BRAND",
            from_entity_column="entity_from",
            to_entity_column="brand",
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
        actual_relationships = client.relationship_api.list_relationships(
            "relationshipTypes/test.HAS_BRAND"
        )
        self.assertCountEqual(expected_relationships, actual_relationships)
        self.assertIsInstance(result, FileLoadingResult)
        self.assertIsInstance(result, CsvLoadingResult)

    def test_load_relationships_only_entity_from_column_specified(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as exception_context:
            CsvRelationshipLoader(client).load_relationships(
                filename="exabel_data_sdk/tests/resources/data/relationships.csv",
                relationship_type="NON_EXISTENT_RELATIONSHIPTYPE",
                from_entity_column="entity_from",
                upsert=False,
            )
        self.assertEqual(
            "Invalid combination of arguments provided: Either both from_entity_column and "
            "to_entity_column must be specified, or neither of them.",
            str(exception_context.exception),
        )

    def test_load_relationships_only_entity_to_column_specified(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as exception_context:
            CsvRelationshipLoader(client).load_relationships(
                filename="exabel_data_sdk/tests/resources/data/relationships.csv",
                relationship_type="NON_EXISTENT_RELATIONSHIPTYPE",
                to_entity_column="BRAND",
                upsert=False,
            )
        self.assertEqual(
            "Invalid combination of arguments provided: Either both from_entity_column and "
            "to_entity_column must be specified, or neither of them.",
            str(exception_context.exception),
        )

    def test_load_relationships_default_entity_from_to_columns(self):
        client: ExabelClient = ExabelMockClient()
        CsvRelationshipLoader(client).load_relationships(
            filename="exabel_data_sdk/tests/resources/data/relationships_with_properties.csv",
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
        actual_relationships = client.relationship_api.list_relationships(
            "relationshipTypes/test.HAS_BRAND"
        )
        self.assertCountEqual(expected_relationships, actual_relationships)

    def _list_entity_types(self):
        return iter(
            [
                EntityType("entityTypes/BRAND", "", "", False),
                EntityType("entityTypes/company", "", "", False),
                EntityType("entityTypes/ns.company", "", "", False),
                EntityType("entityTypes/ns.brand", "", "", False),
                EntityType("entityTypes/global_entity", "", "", False),
                EntityType("entityTypes/otherns.accessible_entity_type", "", "", False),
            ]
        )

    def _check_load_with_entity_types(
        self,
        mock_reader: mock.MagicMock,
        csv_df: pd.DataFrame,
        relationships: Sequence[Relationship],
        **csv_loader_kwargs,
    ):
        mock_reader.read_file.return_value = csv_df
        client = mock.create_autospec(ExabelClient)
        client.entity_api = mock.create_autospec(EntityApi)
        client.entity_api.search = mock.create_autospec(SearchService)
        client.entity_api.get_entity_type_iterator.side_effect = self._list_entity_types
        client.relationship_api = mock.create_autospec(RelationshipApi)
        client.relationship_api.get_relationship_type.return_value = True
        if "from_identifier_type" in csv_loader_kwargs:
            client.entity_api.search.entities_by_terms.return_value = [
                SearchEntitiesResponse.SearchResult(
                    terms=[SearchTerm(field="isin", query="identifier")],
                    entities=[
                        Entity(
                            name="entityTypes/company/entities/the_company",
                            display_name="The Company",
                        )
                    ],
                )
            ]
        CsvRelationshipLoader(client).load_relationships(
            **csv_loader_kwargs,
        )
        client.relationship_api.bulk_create_relationships.assert_called_once_with(
            relationships,
            threads=DEFAULT_NUMBER_OF_THREADS,
            upsert=False,
            retries=DEFAULT_NUMBER_OF_RETRIES,
            abort_threshold=0.5,
        )

    @mock.patch("exabel_data_sdk.services.csv_relationship_loader.CsvReader")
    def test_load_relationships__with_entity_types(self, mock_reader):
        csv_df = pd.DataFrame([{"from": "entity", "to": "brand"}])
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/ns.HAS_BRAND",
                from_entity="entityTypes/ns.company/entities/ns.entity",
                to_entity="entityTypes/ns.brand/entities/ns.brand",
            )
        ]
        self._check_load_with_entity_types(
            mock_reader,
            csv_df,
            expected_relationships,
            filename="filename",
            namespace="ns",
            relationship_type="ns.HAS_BRAND",
            from_entity_type="ns.company",
            to_entity_type="ns.brand",
        )

    @mock.patch("exabel_data_sdk.services.csv_relationship_loader.CsvReader")
    def test_load_relationships__with_entity_types__from_global_entity_type(self, mock_reader):
        csv_df = pd.DataFrame([{"from": "otherns.entity", "to": "brand"}])
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/ns.HAS_BRAND",
                from_entity="entityTypes/global_entity/entities/otherns.entity",
                to_entity="entityTypes/ns.brand/entities/ns.brand",
            )
        ]
        self._check_load_with_entity_types(
            mock_reader,
            csv_df,
            expected_relationships,
            filename="filename",
            namespace="ns",
            relationship_type="ns.HAS_BRAND",
            from_entity_type="global_entity",
            to_entity_type="ns.brand",
        )

    @mock.patch("exabel_data_sdk.services.csv_relationship_loader.CsvReader")
    def test_load_relationships__with_entity_types__to_entity_type_in_accessible_namespace(
        self, mock_reader
    ):
        csv_df = pd.DataFrame([{"from": "entity", "to": "brand"}])
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/ns.HAS_BRAND",
                from_entity=(
                    "entityTypes/otherns.accessible_entity_type/" "entities/otherns.entity"
                ),
                to_entity="entityTypes/ns.brand/entities/ns.brand",
            )
        ]
        self._check_load_with_entity_types(
            mock_reader,
            csv_df,
            expected_relationships,
            filename="filename",
            namespace="ns",
            relationship_type="ns.HAS_BRAND",
            from_entity_type="otherns.accessible_entity_type",
            to_entity_type="ns.brand",
        )

    @mock.patch("exabel_data_sdk.services.csv_relationship_loader.CsvReader")
    def test_load_relationships__with_entity_types__identifier_mappings(self, mock_reader):
        csv_df = pd.DataFrame([{"from": "identifier", "to": "brand"}])
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/ns.HAS_BRAND",
                from_entity="entityTypes/company/entities/the_company",
                to_entity="entityTypes/ns.brand/entities/ns.brand",
            )
        ]
        self._check_load_with_entity_types(
            mock_reader,
            csv_df,
            expected_relationships,
            filename="filename",
            namespace="ns",
            relationship_type="ns.HAS_BRAND",
            from_entity_type="company",
            from_identifier_type="isin",
            to_entity_type="ns.brand",
        )

    @mock.patch("exabel_data_sdk.services.csv_relationship_loader.CsvReader")
    def test_load_relationships__with_entity_types__same_type(self, mock_reader):
        csv_df = pd.DataFrame([{"from": "a_brand", "to": "another_brand"}])
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/ns.ARE_EQUIVALENT",
                from_entity="entityTypes/ns.brand/entities/ns.a_brand",
                to_entity="entityTypes/ns.brand/entities/ns.another_brand",
            )
        ]
        self._check_load_with_entity_types(
            mock_reader,
            csv_df,
            expected_relationships,
            filename="filename",
            namespace="ns",
            relationship_type="ns.ARE_EQUIVALENT",
            from_entity_type="ns.brand",
            to_entity_type="ns.brand",
        )

    @mock.patch("exabel_data_sdk.services.csv_relationship_loader.CsvReader")
    def test_load_relationships__with_entity_types__same_global_type(self, mock_reader):
        csv_df = pd.DataFrame([{"from": "a_company", "to": "another_company"}])
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/ns.ARE_EQUIVALENT",
                from_entity="entityTypes/company/entities/a_company",
                to_entity="entityTypes/company/entities/another_company",
            )
        ]
        self._check_load_with_entity_types(
            mock_reader,
            csv_df,
            expected_relationships,
            filename="filename",
            namespace="ns",
            relationship_type="ns.ARE_EQUIVALENT",
            from_entity_type="company",
            to_entity_type="company",
        )

    @mock.patch("exabel_data_sdk.services.csv_relationship_loader.CsvReader")
    def test_load_relationships__with_entity_types__same_identifier_type(self, mock_reader):
        csv_df = pd.DataFrame([{"from": "identifier", "to": "identifier"}])
        expected_relationships = [
            Relationship(
                relationship_type="relationshipTypes/ns.POINTS_TO_SELF",
                from_entity="entityTypes/company/entities/the_company",
                to_entity="entityTypes/company/entities/the_company",
            )
        ]
        self._check_load_with_entity_types(
            mock_reader,
            csv_df,
            expected_relationships,
            filename="filename",
            namespace="ns",
            relationship_type="ns.POINTS_TO_SELF",
            from_entity_type="company",
            from_identifier_type="isin",
            to_entity_type="company",
            to_identifier_type="isin",
        )

    @mock.patch("exabel_data_sdk.services.csv_reader.CsvReader.read_file")
    def test_load_relationships__with_batch_size(self, mock_read_file: mock.MagicMock):
        df = pd.DataFrame([{"column": "value"}])
        mock_read_file.side_effect = [df, (df for _ in range(2))]
        client = mock.create_autospec(ExabelClient)
        client.relationship_api = mock.create_autospec(RelationshipApi)
        loader = CsvRelationshipLoader(client)
        with mock.patch.object(loader, "_load_relationships") as mock_load:
            loader.load_relationships(
                filename="file",
                relationship_type="relationship_type",
                batch_size=1,
            )
        self.assertIsNone(mock_read_file.call_args_list[0][1].get("chunksize"))
        self.assertEqual(mock_read_file.call_args_list[1][1]["chunksize"], 1)
        self.assertEqual(mock_load.call_count, 2)
