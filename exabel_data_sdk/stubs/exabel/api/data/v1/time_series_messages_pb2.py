"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....exabel.api.time import time_range_pb2 as exabel_dot_api_dot_time_dot_time__range__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.type import decimal_pb2 as google_dot_type_dot_decimal__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-exabel/api/data/v1/time_series_messages.proto\x12\x12exabel.api.data.v1\x1a exabel/api/time/time_range.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x19google/type/decimal.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x84\x02\n\nTimeSeries\x12x\n\x04name\x18\x01 \x01(\tBj\x92AbJL"entityTypes/store/entities/ns.apple_store_fifth_avenue/signals/ns.visitors"\xca>\x11\xfa\x02\x0etimeSeriesName\xe2A\x02\x05\x02\x123\n\x06points\x18\x02 \x03(\x0b2#.exabel.api.data.v1.TimeSeriesPoint\x12\x17\n\tread_only\x18\x03 \x01(\x08B\x04\xe2A\x01\x03\x12.\n\x05units\x18\x04 \x01(\x0b2\x19.exabel.api.data.v1.UnitsB\x04\xe2A\x01\x01"\x9e\x01\n\x0fTimeSeriesPoint\x12.\n\x04time\x18\x01 \x01(\x0b2\x1a.google.protobuf.TimestampB\x04\xe2A\x01\x02\x12+\n\x05value\x18\x02 \x01(\x0b2\x1c.google.protobuf.DoubleValue\x12.\n\nknown_time\x18\x03 \x01(\x0b2\x1a.google.protobuf.Timestamp"v\n\x0eTimeSeriesView\x12.\n\ntime_range\x18\x01 \x01(\x0b2\x1a.exabel.api.time.TimeRange\x124\n\nknown_time\x18\x02 \x01(\x0b2\x1a.google.protobuf.TimestampB\x04\xe2A\x01\x01"\x9f\x01\n\x10DefaultKnownTime\x12\x16\n\x0ccurrent_time\x18\x01 \x01(\x08H\x00\x120\n\nknown_time\x18\x02 \x01(\x0b2\x1a.google.protobuf.TimestampH\x00\x120\n\x0btime_offset\x18\x03 \x01(\x0b2\x19.google.protobuf.DurationH\x00B\x0f\n\rspecification"\x83\x01\n\x05Units\x12.\n\x05units\x18\x01 \x03(\x0b2\x18.exabel.api.data.v1.UnitB\x05\xe2A\x02\x01\x05\x12/\n\nmultiplier\x18\x02 \x01(\x0b2\x14.google.type.DecimalB\x05\xe2A\x02\x01\x05\x12\x19\n\x0bdescription\x18\x03 \x01(\tB\x04\xe2A\x01\x01"\xec\x01\n\x04Unit\x12<\n\tdimension\x18\x01 \x01(\x0e2".exabel.api.data.v1.Unit.DimensionB\x05\xe2A\x02\x01\x05\x12\x13\n\x04unit\x18\x02 \x01(\tB\x05\xe2A\x02\x02\x05\x12\x17\n\x08exponent\x18\x03 \x01(\x11B\x05\xe2A\x02\x01\x05"x\n\tDimension\x12\x15\n\x11DIMENSION_UNKNOWN\x10\x00\x12\x16\n\x12DIMENSION_CURRENCY\x10\x01\x12\x12\n\x0eDIMENSION_MASS\x10\x02\x12\x14\n\x10DIMENSION_LENGTH\x10\x03\x12\x12\n\x0eDIMENSION_TIME\x10\x04BK\n\x16com.exabel.api.data.v1B\x17TimeSeriesMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.time_series_messages_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals['DESCRIPTOR']._options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x17TimeSeriesMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_TIMESERIES'].fields_by_name['name']._options = None
    _globals['_TIMESERIES'].fields_by_name['name']._serialized_options = b'\x92AbJL"entityTypes/store/entities/ns.apple_store_fifth_avenue/signals/ns.visitors"\xca>\x11\xfa\x02\x0etimeSeriesName\xe2A\x02\x05\x02'
    _globals['_TIMESERIES'].fields_by_name['read_only']._options = None
    _globals['_TIMESERIES'].fields_by_name['read_only']._serialized_options = b'\xe2A\x01\x03'
    _globals['_TIMESERIES'].fields_by_name['units']._options = None
    _globals['_TIMESERIES'].fields_by_name['units']._serialized_options = b'\xe2A\x01\x01'
    _globals['_TIMESERIESPOINT'].fields_by_name['time']._options = None
    _globals['_TIMESERIESPOINT'].fields_by_name['time']._serialized_options = b'\xe2A\x01\x02'
    _globals['_TIMESERIESVIEW'].fields_by_name['known_time']._options = None
    _globals['_TIMESERIESVIEW'].fields_by_name['known_time']._serialized_options = b'\xe2A\x01\x01'
    _globals['_UNITS'].fields_by_name['units']._options = None
    _globals['_UNITS'].fields_by_name['units']._serialized_options = b'\xe2A\x02\x01\x05'
    _globals['_UNITS'].fields_by_name['multiplier']._options = None
    _globals['_UNITS'].fields_by_name['multiplier']._serialized_options = b'\xe2A\x02\x01\x05'
    _globals['_UNITS'].fields_by_name['description']._options = None
    _globals['_UNITS'].fields_by_name['description']._serialized_options = b'\xe2A\x01\x01'
    _globals['_UNIT'].fields_by_name['dimension']._options = None
    _globals['_UNIT'].fields_by_name['dimension']._serialized_options = b'\xe2A\x02\x01\x05'
    _globals['_UNIT'].fields_by_name['unit']._options = None
    _globals['_UNIT'].fields_by_name['unit']._serialized_options = b'\xe2A\x02\x02\x05'
    _globals['_UNIT'].fields_by_name['exponent']._options = None
    _globals['_UNIT'].fields_by_name['exponent']._serialized_options = b'\xe2A\x02\x01\x05'
    _globals['_TIMESERIES']._serialized_start = 309
    _globals['_TIMESERIES']._serialized_end = 569
    _globals['_TIMESERIESPOINT']._serialized_start = 572
    _globals['_TIMESERIESPOINT']._serialized_end = 730
    _globals['_TIMESERIESVIEW']._serialized_start = 732
    _globals['_TIMESERIESVIEW']._serialized_end = 850
    _globals['_DEFAULTKNOWNTIME']._serialized_start = 853
    _globals['_DEFAULTKNOWNTIME']._serialized_end = 1012
    _globals['_UNITS']._serialized_start = 1015
    _globals['_UNITS']._serialized_end = 1146
    _globals['_UNIT']._serialized_start = 1149
    _globals['_UNIT']._serialized_end = 1385
    _globals['_UNIT_DIMENSION']._serialized_start = 1265
    _globals['_UNIT_DIMENSION']._serialized_end = 1385