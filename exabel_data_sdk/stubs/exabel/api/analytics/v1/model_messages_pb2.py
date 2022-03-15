"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='exabel/api/analytics/v1/model_messages.proto', package='exabel.api.analytics.v1', syntax='proto3', serialized_options=b'\n\x1bcom.exabel.api.analytics.v1B\x12ModelMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1', create_key=_descriptor._internal_create_key, serialized_pb=b'\n,exabel/api/analytics/v1/model_messages.proto\x12\x17exabel.api.analytics.v1\x1a\x1fgoogle/api/field_behavior.proto"2\n\x08ModelRun\x12\x11\n\x04name\x18\x01 \x01(\tB\x03\xe0A\x03\x12\x13\n\x0bdescription\x18\x02 \x01(\tBP\n\x1bcom.exabel.api.analytics.v1B\x12ModelMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3', dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR])
_MODELRUN = _descriptor.Descriptor(name='ModelRun', full_name='exabel.api.analytics.v1.ModelRun', filename=None, file=DESCRIPTOR, containing_type=None, create_key=_descriptor._internal_create_key, fields=[_descriptor.FieldDescriptor(name='name', full_name='exabel.api.analytics.v1.ModelRun.name', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=b''.decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=b'\xe0A\x03', file=DESCRIPTOR, create_key=_descriptor._internal_create_key), _descriptor.FieldDescriptor(name='description', full_name='exabel.api.analytics.v1.ModelRun.description', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=b''.decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=106, serialized_end=156)
DESCRIPTOR.message_types_by_name['ModelRun'] = _MODELRUN
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
ModelRun = _reflection.GeneratedProtocolMessageType('ModelRun', (_message.Message,), {'DESCRIPTOR': _MODELRUN, '__module__': 'exabel.api.analytics.v1.model_messages_pb2'})
_sym_db.RegisterMessage(ModelRun)
DESCRIPTOR._options = None
_MODELRUN.fields_by_name['name']._options = None