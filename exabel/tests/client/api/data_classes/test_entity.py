from exabel.client.api.data_classes.entity import Entity


class TestEntity:
    def test_proto_conversion(self):
        entity = Entity(
            name="entityTypes/country/entities/no",
            display_name="Norway",
            description="Country Norway",
            properties={"a": False, "b": 3.5, "c": "c_value"},
        )
        assert entity == Entity.from_proto(entity.to_proto())
