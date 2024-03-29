"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright (c) 2019-2022 Exabel AS. All rights reserved."""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class TimeRange(google.protobuf.message.Message):
    """A time range represented by two google.protobuf.Timestamps. The default time range includes the
    start point and excludes the end point.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    FROM_TIME_FIELD_NUMBER: builtins.int
    EXCLUDE_FROM_FIELD_NUMBER: builtins.int
    TO_TIME_FIELD_NUMBER: builtins.int
    INCLUDE_TO_FIELD_NUMBER: builtins.int

    @property
    def from_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Start of the time range, *included* in the range by default."""
    exclude_from: builtins.bool
    'Set to `true` to exclude the start point from the range.'

    @property
    def to_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """End of the time range, *excluded* from the range by default."""
    include_to: builtins.bool
    'Set to `true` to include the end point in the range.'

    def __init__(self, *, from_time: google.protobuf.timestamp_pb2.Timestamp | None=..., exclude_from: builtins.bool | None=..., to_time: google.protobuf.timestamp_pb2.Timestamp | None=..., include_to: builtins.bool | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['from_time', b'from_time', 'to_time', b'to_time']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['exclude_from', b'exclude_from', 'from_time', b'from_time', 'include_to', b'include_to', 'to_time', b'to_time']) -> None:
        ...
global___TimeRange = TimeRange