from datetime import datetime

from dateutil import tz

from exabel.client.api.data_classes.tag import Tag, TagMetaData


class TestTag:
    def test_proto_conversion(self):
        tag = Tag(
            name="tags/user:123",
            display_name="My tag",
            description="My tag description",
            entity_type="entityTypes/company",
            metadata=TagMetaData(
                create_time=datetime(2022, 3, 3, tzinfo=tz.tzutc()),
                update_time=datetime(2022, 4, 2, tzinfo=tz.tzutc()),
                created_by="users/123",
                updated_by="users/234",
                write_access=True,
            ),
        )
        assert tag == Tag.from_proto(tag.to_proto())
