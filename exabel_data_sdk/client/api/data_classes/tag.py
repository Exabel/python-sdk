from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dateutil import tz
from google.protobuf.timestamp_pb2 import Timestamp as ProtoTimestamp

from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import ItemMetadata as ProtoTagMetadata
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import Tag as ProtoTag


@dataclass
class TagMetaData:
    """
    Metadata of a tag.

    Attributes:
        create_time:   Time when the tag was created.
        update_time:   Time when the tag was updaed.
        created_by:    Resource name of the user that created the tag.
        updated_by:    Resource name of the user that updated the tag.
        write_access:  Whether the current user has write access to the tag.
    """

    create_time: Optional[datetime]
    update_time: Optional[datetime]
    created_by: Optional[str]
    updated_by: Optional[str]
    write_access: Optional[bool]

    @classmethod
    def from_proto(cls, metadata: ProtoTagMetadata) -> "TagMetaData":
        """Create a TagMetaData from the given protobuf TagMetadata."""
        return TagMetaData(
            create_time=cls._proto_timestamp_to_datetime(metadata.create_time),
            update_time=cls._proto_timestamp_to_datetime(metadata.update_time),
            created_by=metadata.created_by,
            updated_by=metadata.updated_by,
            write_access=metadata.write_access,
        )

    def to_proto(self) -> ProtoTagMetadata:
        """Create a protobuf TagMetadata from this TagMetadata."""
        return ProtoTagMetadata(
            create_time=self._datetime_to_proto_timestamp(self.create_time),
            update_time=self._datetime_to_proto_timestamp(self.update_time),
            created_by=self.created_by,
            updated_by=self.updated_by,
            write_access=self.write_access,
        )

    @staticmethod
    def _proto_timestamp_to_datetime(timestamp: ProtoTimestamp) -> Optional[datetime]:
        return datetime.fromtimestamp(timestamp.seconds, tz=tz.tzutc())

    @staticmethod
    def _datetime_to_proto_timestamp(date: Optional[datetime]) -> Optional[ProtoTimestamp]:
        if date is None:
            return date
        timestamp = ProtoTimestamp()
        timestamp.seconds = int(date.timestamp())
        return timestamp


@dataclass
class Tag:
    """
    A tag in the Analytics API.

    Attributes:
        name:           The resource name of the tag, for example "tags/user:123".
                        The resource name is not namespaced. It is required in all operations
                        except the create and list tags operations.
        display_name:   The display name of the tag.
        description:    The description of the tag.
        entity_type:    The entity type resource name specifying the type of entities this tag can
                        contain. It is set by the backend when the first entity is tagged.
        metadata:       Metadata of the tag.
    """

    name: Optional[str]
    display_name: str
    description: Optional[str]
    entity_type: Optional[str] = None
    metadata: Optional[TagMetaData] = None

    @staticmethod
    def from_proto(tag: ProtoTag) -> "Tag":
        """Create a Tag from the given protobuf Tag."""
        return Tag(
            name=tag.name,
            display_name=tag.display_name,
            description=tag.description,
            entity_type=tag.entity_type,
            metadata=TagMetaData.from_proto(metadata=tag.metadata),
        )

    def to_proto(self) -> ProtoTag:
        """Create a protobuf Tag from this Tag."""
        return ProtoTag(
            name=self.name,
            display_name=self.display_name,
            description=self.description,
            entity_type=self.entity_type,
            metadata=self.metadata.to_proto() if self.metadata else None,
        )
