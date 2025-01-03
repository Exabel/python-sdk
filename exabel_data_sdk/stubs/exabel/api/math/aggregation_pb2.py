"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/math/aggregation.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!exabel/api/math/aggregation.proto\x12\x0fexabel.api.math*l\n\x0bAggregation\x12\x17\n\x13AGGREGATION_INVALID\x10\x00\x12\x08\n\x04MEAN\x10\x01\x12\t\n\x05FIRST\x10\x02\x12\x08\n\x04LAST\x10\x03\x12\x07\n\x03SUM\x10\x04\x12\x07\n\x03MIN\x10\x05\x12\x07\n\x03MAX\x10\x06\x12\n\n\x06MEDIAN\x10\x07B>\n\x13com.exabel.api.mathB\x10AggregationProtoP\x01Z\x13exabel.com/api/mathb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.math.aggregation_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x13com.exabel.api.mathB\x10AggregationProtoP\x01Z\x13exabel.com/api/math'
    _globals['_AGGREGATION']._serialized_start = 54
    _globals['_AGGREGATION']._serialized_end = 162