import unittest

from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType


class TestRelationshipType(unittest.TestCase):
    def test_proto_conversion(self):
        relationship_type = RelationshipType(
            name="relationshipTypes/ns1.owned_by",
            description="description",
            properties={"a": False, "b": 3.5, "c": "c_value"},
        )
        self.assertEqual(
            relationship_type, RelationshipType.from_proto(relationship_type.to_proto())
        )
