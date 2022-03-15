"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from exabel.api.time.time_range_pb2 import TimeRange as exabel___api___time___time_range_pb2___TimeRange
from google.protobuf.descriptor import Descriptor as google___protobuf___descriptor___Descriptor, FileDescriptor as google___protobuf___descriptor___FileDescriptor
from google.protobuf.duration_pb2 import Duration as google___protobuf___duration_pb2___Duration
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer
from google.protobuf.message import Message as google___protobuf___message___Message
from google.protobuf.timestamp_pb2 import Timestamp as google___protobuf___timestamp_pb2___Timestamp
from google.protobuf.wrappers_pb2 import DoubleValue as google___protobuf___wrappers_pb2___DoubleValue
from typing import Iterable as typing___Iterable, Optional as typing___Optional, Text as typing___Text
from typing_extensions import Literal as typing_extensions___Literal
builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int
DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

class TimeSeries(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    name: typing___Text = ...
    read_only: builtin___bool = ...

    @property
    def points(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___TimeSeriesPoint]:
        ...

    def __init__(self, *, name: typing___Optional[typing___Text]=None, points: typing___Optional[typing___Iterable[type___TimeSeriesPoint]]=None, read_only: typing___Optional[builtin___bool]=None) -> None:
        ...

    def ClearField(self, field_name: typing_extensions___Literal[u'name', b'name', u'points', b'points', u'read_only', b'read_only']) -> None:
        ...
type___TimeSeries = TimeSeries

class TimeSeriesPoint(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def time(self) -> google___protobuf___timestamp_pb2___Timestamp:
        ...

    @property
    def value(self) -> google___protobuf___wrappers_pb2___DoubleValue:
        ...

    @property
    def known_time(self) -> google___protobuf___timestamp_pb2___Timestamp:
        ...

    def __init__(self, *, time: typing___Optional[google___protobuf___timestamp_pb2___Timestamp]=None, value: typing___Optional[google___protobuf___wrappers_pb2___DoubleValue]=None, known_time: typing___Optional[google___protobuf___timestamp_pb2___Timestamp]=None) -> None:
        ...

    def HasField(self, field_name: typing_extensions___Literal[u'known_time', b'known_time', u'time', b'time', u'value', b'value']) -> builtin___bool:
        ...

    def ClearField(self, field_name: typing_extensions___Literal[u'known_time', b'known_time', u'time', b'time', u'value', b'value']) -> None:
        ...
type___TimeSeriesPoint = TimeSeriesPoint

class TimeSeriesView(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def time_range(self) -> exabel___api___time___time_range_pb2___TimeRange:
        ...

    @property
    def known_time(self) -> google___protobuf___timestamp_pb2___Timestamp:
        ...

    def __init__(self, *, time_range: typing___Optional[exabel___api___time___time_range_pb2___TimeRange]=None, known_time: typing___Optional[google___protobuf___timestamp_pb2___Timestamp]=None) -> None:
        ...

    def HasField(self, field_name: typing_extensions___Literal[u'known_time', b'known_time', u'time_range', b'time_range']) -> builtin___bool:
        ...

    def ClearField(self, field_name: typing_extensions___Literal[u'known_time', b'known_time', u'time_range', b'time_range']) -> None:
        ...
type___TimeSeriesView = TimeSeriesView

class DefaultKnownTime(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    current_time: builtin___bool = ...

    @property
    def known_time(self) -> google___protobuf___timestamp_pb2___Timestamp:
        ...

    @property
    def time_offset(self) -> google___protobuf___duration_pb2___Duration:
        ...

    def __init__(self, *, current_time: typing___Optional[builtin___bool]=None, known_time: typing___Optional[google___protobuf___timestamp_pb2___Timestamp]=None, time_offset: typing___Optional[google___protobuf___duration_pb2___Duration]=None) -> None:
        ...

    def HasField(self, field_name: typing_extensions___Literal[u'current_time', b'current_time', u'known_time', b'known_time', u'specification', b'specification', u'time_offset', b'time_offset']) -> builtin___bool:
        ...

    def ClearField(self, field_name: typing_extensions___Literal[u'current_time', b'current_time', u'known_time', b'known_time', u'specification', b'specification', u'time_offset', b'time_offset']) -> None:
        ...

    def WhichOneof(self, oneof_group: typing_extensions___Literal[u'specification', b'specification']) -> typing_extensions___Literal['current_time', 'known_time', 'time_offset']:
        ...
type___DefaultKnownTime = DefaultKnownTime