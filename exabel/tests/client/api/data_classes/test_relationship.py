from exabel.client.api.data_classes.relationship import Relationship


class TestRelationship:
    def test_proto_conversion(self):
        relationship = Relationship(
            relationship_type="relationshipTypes/ns1.owned_by",
            from_entity="entityTypes/ns1.store/entities/ns1.store1",
            to_entity="entityTypes/company/entities/companyA",
            description="description",
            properties={"a": False, "b": 3.5, "c": "c_value"},
        )
        assert relationship == Relationship.from_proto(relationship.to_proto())
