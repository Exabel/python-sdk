import unittest

from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.relationship_api import RelationshipApi
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
