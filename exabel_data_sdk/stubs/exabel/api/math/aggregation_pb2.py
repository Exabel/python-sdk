"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='exabel/api/math/aggregation.proto', package='exabel.api.math', syntax='proto3', serialized_options=b'\n\x13com.exabel.api.mathB\x10AggregationProtoP\x01Z\x13exabel.com/api/math', create_key=_descriptor._internal_create_key, serialized_pb=b'\n!exabel/api/math/aggregation.proto\x12\x0fexabel.api.math*`\n\x0bAggregation\x12\x17\n\x13AGGREGATION_INVALID\x10\x00\x12\x08\n\x04MEAN\x10\x01\x12\t\n\x05FIRST\x10\x02\x12\x08\n\x04LAST\x10\x03\x12\x07\n\x03SUM\x10\x04\x12\x07\n\x03MIN\x10\x05\x12\x07\n\x03MAX\x10\x06B>\n\x13com.exabel.api.mathB\x10AggregationProtoP\x01Z\x13exabel.com/api/mathb\x06proto3')
_AGGREGATION = _descriptor.EnumDescriptor(name='Aggregation', full_name='exabel.api.math.Aggregation', filename=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key, values=[_descriptor.EnumValueDescriptor(name='AGGREGATION_INVALID', index=0, number=0, serialized_options=None, type=None, create_key=_descriptor._internal_create_key), _descriptor.EnumValueDescriptor(name='MEAN', index=1, number=1, serialized_options=None, type=None, create_key=_descriptor._internal_create_key), _descriptor.EnumValueDescriptor(name='FIRST', index=2, number=2, serialized_options=None, type=None, create_key=_descriptor._internal_create_key), _descriptor.EnumValueDescriptor(name='LAST', index=3, number=3, serialized_options=None, type=None, create_key=_descriptor._internal_create_key), _descriptor.EnumValueDescriptor(name='SUM', index=4, number=4, serialized_options=None, type=None, create_key=_descriptor._internal_create_key), _descriptor.EnumValueDescriptor(name='MIN', index=5, number=5, serialized_options=None, type=None, create_key=_descriptor._internal_create_key), _descriptor.EnumValueDescriptor(name='MAX', index=6, number=6, serialized_options=None, type=None, create_key=_descriptor._internal_create_key)], containing_type=None, serialized_options=None, serialized_start=54, serialized_end=150)
_sym_db.RegisterEnumDescriptor(_AGGREGATION)
Aggregation = enum_type_wrapper.EnumTypeWrapper(_AGGREGATION)
AGGREGATION_INVALID = 0
MEAN = 1
FIRST = 2
LAST = 3
SUM = 4
MIN = 5
MAX = 6
DESCRIPTOR.enum_types_by_name['Aggregation'] = _AGGREGATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
DESCRIPTOR._options = None