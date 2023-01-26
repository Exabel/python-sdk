import unittest
from unittest import mock

from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.relationship_api import RelationshipApi
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.tests.client.api.mock_relationship_api import MockRelationshipApi

AMAZON = "entityTypes/company/entities/Amazon"
USA = "entityTypes/country/entities/USA"
RELATIONHIP_TYPE = "relationshipTypes/LOCATED_IN"


class TestRelationshipApi(unittest.TestCase):
    def test_upsert(self):
        relationship_api: RelationshipApi = MockRelationshipApi()
        expected = Relationship(
            relationship_type=RELATIONHIP_TYPE,
            from_entity=AMAZON,
            to_entity=USA,
        )
        created_relationship = relationship_api.upsert_relationship(expected)
        self.assertEqual(expected, created_relationship)
        updated_relationship = relationship_api.upsert_relationship(expected)
        self.assertEqual(expected, updated_relationship)

    def test_upsert_replaces_resource(self):
        relationship_api: RelationshipApi = MockRelationshipApi()
        old_relationship = Relationship(
            relationship_type=RELATIONHIP_TYPE,
            from_entity=AMAZON,
            to_entity=USA,
            description="Old relationship description",
            properties={"old_property": "old_value"},
        )
        expected = Relationship(
            relationship_type=RELATIONHIP_TYPE,
            from_entity=AMAZON,
            to_entity=USA,
            description="New relationship description",
        )
        relationship_api.create_relationship(old_relationship)
        relationship_api.upsert_relationship(expected)
        actual_relationship = relationship_api.get_relationship(
            expected.relationship_type, expected.from_entity, expected.to_entity
        )
        self.assertEqual(expected, actual_relationship)

    def test_get_relationships_from_entity_iterator(self):
        relationship_api = RelationshipApi(ClientConfig("api-key"))
        relationship_1 = mock.create_autospec(Relationship)
        relationship_2 = mock.create_autospec(Relationship)
        relationship_3 = mock.create_autospec(Relationship)
        relationship_api.get_relationships_from_entity = mock.MagicMock()
        relationship_api.get_relationships_from_entity.side_effect = [
            PagingResult([relationship_1], next_page_token="1", total_size=3),
            PagingResult([relationship_2], next_page_token="2", total_size=3),
            PagingResult([relationship_3], next_page_token=None, total_size=3),
            AssertionError("Should not be called"),
        ]
        relationships = list(
            relationship_api.get_relationships_from_entity_iterator("relationship_type", "entity")
        )
        self.assertEqual(3, len(relationships))
        self.assertSequenceEqual([relationship_1, relationship_2, relationship_3], relationships)
        relationship_api.get_relationships_from_entity.assert_has_calls(
            [
                mock.call(
                    relationship_type="relationship_type", from_entity="entity", page_token=None
                ),
                mock.call(
                    relationship_type="relationship_type", from_entity="entity", page_token="1"
                ),
                mock.call(
                    relationship_type="relationship_type", from_entity="entity", page_token="2"
                ),
            ]
        )

    def test_get_relationships_to_entity_iterator(self):
        relationship_api = RelationshipApi(ClientConfig("api-key"))
        relationship_1 = mock.create_autospec(Relationship)
        relationship_2 = mock.create_autospec(Relationship)
        relationship_3 = mock.create_autospec(Relationship)
        relationship_api.get_relationships_to_entity = mock.MagicMock()
        relationship_api.get_relationships_to_entity.side_effect = [
            PagingResult([relationship_1], next_page_token="1", total_size=3),
            PagingResult([relationship_2], next_page_token="2", total_size=3),
            PagingResult([relationship_3], next_page_token=None, total_size=3),
            AssertionError("Should not be called"),
        ]
        relationships = list(
            relationship_api.get_relationships_to_entity_iterator("relationship_type", "entity")
        )
        self.assertEqual(3, len(relationships))
        self.assertSequenceEqual([relationship_1, relationship_2, relationship_3], relationships)
        relationship_api.get_relationships_to_entity.assert_has_calls(
            [
                mock.call(
                    relationship_type="relationship_type", to_entity="entity", page_token=None
                ),
                mock.call(
                    relationship_type="relationship_type", to_entity="entity", page_token="1"
                ),
                mock.call(
                    relationship_type="relationship_type", to_entity="entity", page_token="2"
                ),
            ]
        )

    def test_get_relationships_iterator(self):
        relationship_api = RelationshipApi(ClientConfig("api-key"))
        relationship_1 = mock.create_autospec(Relationship)
        relationship_2 = mock.create_autospec(Relationship)
        relationship_3 = mock.create_autospec(Relationship)
        relationship_api.list_relationships = mock.MagicMock()
        relationship_api.list_relationships.side_effect = [
            PagingResult([relationship_1], next_page_token="1", total_size=3),
            PagingResult([relationship_2], next_page_token="2", total_size=3),
            PagingResult([relationship_3], next_page_token=None, total_size=3),
            AssertionError("Should not be called"),
        ]
        relationships = list(relationship_api.get_relationships_iterator("relationship_type"))
        self.assertEqual(3, len(relationships))
        self.assertSequenceEqual([relationship_1, relationship_2, relationship_3], relationships)
        relationship_api.list_relationships.assert_has_calls(
            [
                mock.call(relationship_type="relationship_type", page_token=None),
                mock.call(relationship_type="relationship_type", page_token="1"),
                mock.call(relationship_type="relationship_type", page_token="2"),
            ]
        )
