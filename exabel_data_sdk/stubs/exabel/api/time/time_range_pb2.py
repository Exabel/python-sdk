"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/time/time_range.proto')
_sym_db = _symbol_database.Default()
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n exabel/api/time/time_range.proto\x12\x0fexabel.api.time\x1a\x1fgoogle/protobuf/timestamp.proto"\x91\x01\n\tTimeRange\x12-\n\tfrom_time\x18\x01 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x14\n\x0cexclude_from\x18\x02 \x01(\x08\x12+\n\x07to_time\x18\x03 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x12\n\ninclude_to\x18\x04 \x01(\x08B<\n\x13com.exabel.api.timeB\x0eTimeRangeProtoP\x01Z\x13exabel.com/api/timeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.time.time_range_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x13com.exabel.api.timeB\x0eTimeRangeProtoP\x01Z\x13exabel.com/api/time'
    _globals['_TIMERANGE']._serialized_start = 87
    _globals['_TIMERANGE']._serialized_end = 232