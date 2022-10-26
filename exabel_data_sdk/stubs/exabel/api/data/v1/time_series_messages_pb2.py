"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....exabel.api.time import time_range_pb2 as exabel_dot_api_dot_time_dot_time__range__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-exabel/api/data/v1/time_series_messages.proto\x12\x12exabel.api.data.v1\x1a exabel/api/time/time_range.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xd4\x01\n\nTimeSeries\x12y\n\x04name\x18\x01 \x01(\tBk\xe0A\x05\xe0A\x02\x92AbJL"entityTypes/store/entities/ns.apple_store_fifth_avenue/signals/ns.visitors"\xca>\x11\xfa\x02\x0etimeSeriesName\x123\n\x06points\x18\x02 \x03(\x0b2#.exabel.api.data.v1.TimeSeriesPoint\x12\x16\n\tread_only\x18\x03 \x01(\x08B\x03\xe0A\x03"\x9d\x01\n\x0fTimeSeriesPoint\x12-\n\x04time\x18\x01 \x01(\x0b2\x1a.google.protobuf.TimestampB\x03\xe0A\x02\x12+\n\x05value\x18\x02 \x01(\x0b2\x1c.google.protobuf.DoubleValue\x12.\n\nknown_time\x18\x03 \x01(\x0b2\x1a.google.protobuf.Timestamp"u\n\x0eTimeSeriesView\x12.\n\ntime_range\x18\x01 \x01(\x0b2\x1a.exabel.api.time.TimeRange\x123\n\nknown_time\x18\x02 \x01(\x0b2\x1a.google.protobuf.TimestampB\x03\xe0A\x01"\x9f\x01\n\x10DefaultKnownTime\x12\x16\n\x0ccurrent_time\x18\x01 \x01(\x08H\x00\x120\n\nknown_time\x18\x02 \x01(\x0b2\x1a.google.protobuf.TimestampH\x00\x120\n\x0btime_offset\x18\x03 \x01(\x0b2\x19.google.protobuf.DurationH\x00B\x0f\n\rspecificationBK\n\x16com.exabel.api.data.v1B\x17TimeSeriesMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.time_series_messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x17TimeSeriesMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _TIMESERIES.fields_by_name['name']._options = None
    _TIMESERIES.fields_by_name['name']._serialized_options = b'\xe0A\x05\xe0A\x02\x92AbJL"entityTypes/store/entities/ns.apple_store_fifth_avenue/signals/ns.visitors"\xca>\x11\xfa\x02\x0etimeSeriesName'
    _TIMESERIES.fields_by_name['read_only']._options = None
    _TIMESERIES.fields_by_name['read_only']._serialized_options = b'\xe0A\x03'
    _TIMESERIESPOINT.fields_by_name['time']._options = None
    _TIMESERIESPOINT.fields_by_name['time']._serialized_options = b'\xe0A\x02'
    _TIMESERIESVIEW.fields_by_name['known_time']._options = None
    _TIMESERIESVIEW.fields_by_name['known_time']._serialized_options = b'\xe0A\x01'
    _TIMESERIES._serialized_start = 282
    _TIMESERIES._serialized_end = 494
    _TIMESERIESPOINT._serialized_start = 497
    _TIMESERIESPOINT._serialized_end = 654
    _TIMESERIESVIEW._serialized_start = 656
    _TIMESERIESVIEW._serialized_end = 773
    _DEFAULTKNOWNTIME._serialized_start = 776
    _DEFAULTKNOWNTIME._serialized_end = 935