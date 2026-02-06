from unittest import mock

from exabel.client.api.data_classes.paging_result import PagingResult
from exabel.client.api.data_classes.relationship import Relationship
from exabel.client.api.relationship_api import RelationshipApi
from exabel.client.client_config import ClientConfig
from exabel.tests.client.api.mock_relationship_api import MockRelationshipApi

AMAZON = "entityTypes/company/entities/Amazon"
USA = "entityTypes/country/entities/USA"
RELATIONHIP_TYPE = "relationshipTypes/LOCATED_IN"


class TestRelationshipApi:
    def test_upsert(self):
        relationship_api: RelationshipApi = MockRelationshipApi()
        expected = Relationship(
            relationship_type=RELATIONHIP_TYPE,
            from_entity=AMAZON,
            to_entity=USA,
        )
        created_relationship = relationship_api.upsert_relationship(expected)
        assert expected == created_relationship
        updated_relationship = relationship_api.upsert_relationship(expected)
        assert expected == updated_relationship

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
        assert expected == actual_relationship

    def test_get_relationships_from_entity_iterator(self):
        relationship_api = RelationshipApi(ClientConfig("api-key"))
        relationship = mock.create_autospec(Relationship)
        relationship_api.get_relationships_from_entity = mock.MagicMock()
        relationship_api.get_relationships_from_entity.side_effect = [
            PagingResult([relationship] * 1000, next_page_token="1000", total_size=1100),
            PagingResult([relationship] * 100, next_page_token="~~~", total_size=1100),
            AssertionError("Should not be called"),
        ]
        relationships = list(
            relationship_api.get_relationships_from_entity_iterator("relationship_type", "entity")
        )
        assert 1100 == len(relationships)
        assert [relationship] * 1100 == relationships
        relationship_api.get_relationships_from_entity.assert_has_calls(
            [
                mock.call(
                    relationship_type="relationship_type",
                    from_entity="entity",
                    page_token=None,
                    page_size=1000,
                ),
                mock.call(
                    relationship_type="relationship_type",
                    from_entity="entity",
                    page_token="1000",
                    page_size=1000,
                ),
            ]
        )

    def test_get_relationships_to_entity_iterator(self):
        relationship_api = RelationshipApi(ClientConfig("api-key"))
        relationship = mock.create_autospec(Relationship)
        relationship_api.get_relationships_to_entity = mock.MagicMock()
        relationship_api.get_relationships_to_entity.side_effect = [
            PagingResult([relationship] * 1000, next_page_token="1000", total_size=1100),
            PagingResult([relationship] * 100, next_page_token="~~~", total_size=1100),
            AssertionError("Should not be called"),
        ]
        relationships = list(
            relationship_api.get_relationships_to_entity_iterator("relationship_type", "entity")
        )
        assert 1100 == len(relationships)
        assert [relationship] * 1100 == relationships
        relationship_api.get_relationships_to_entity.assert_has_calls(
            [
                mock.call(
                    relationship_type="relationship_type",
                    to_entity="entity",
                    page_token=None,
                    page_size=1000,
                ),
                mock.call(
                    relationship_type="relationship_type",
                    to_entity="entity",
                    page_token="1000",
                    page_size=1000,
                ),
            ]
        )

    def test_get_relationships_iterator(self):
        relationship_api = RelationshipApi(ClientConfig("api-key"))
        relationship = mock.create_autospec(Relationship)
        relationship_api.list_relationships = mock.MagicMock()
        relationship_api.list_relationships.side_effect = [
            PagingResult([relationship] * 1000, next_page_token="1000", total_size=1100),
            PagingResult([relationship] * 100, next_page_token="~~~", total_size=1100),
            AssertionError("Should not be called"),
        ]
        relationships = list(relationship_api.get_relationships_iterator("relationship_type"))
        assert 1100 == len(relationships)
        assert [relationship] * 1100 == relationships
        relationship_api.list_relationships.assert_has_calls(
            [
                mock.call(relationship_type="relationship_type", page_token=None, page_size=1000),
                mock.call(relationship_type="relationship_type", page_token="1000", page_size=1000),
            ]
        )
