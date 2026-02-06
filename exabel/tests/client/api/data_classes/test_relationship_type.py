from exabel.client.api.data_classes.relationship_type import RelationshipType


class TestRelationshipType:
    def test_proto_conversion(self):
        relationship_type = RelationshipType(
            name="relationshipTypes/ns1.owned_by",
            description="description",
            properties={"a": False, "b": 3.5, "c": "c_value"},
        )
        assert relationship_type == RelationshipType.from_proto(relationship_type.to_proto())
