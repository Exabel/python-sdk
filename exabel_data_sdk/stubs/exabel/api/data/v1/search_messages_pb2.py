"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='exabel/api/data/v1/search_messages.proto', package='exabel.api.data.v1', syntax='proto3', serialized_options=b'\n\x16com.exabel.api.data.v1B\x13SearchMessagesProtoP\x01Z\x16exabel.com/api/data/v1', create_key=_descriptor._internal_create_key, serialized_pb=b'\n(exabel/api/data/v1/search_messages.proto\x12\x12exabel.api.data.v1\x1a\x1fgoogle/api/field_behavior.proto"4\n\nSearchTerm\x12\x12\n\x05field\x18\x01 \x01(\tB\x03\xe0A\x02\x12\x12\n\x05query\x18\x02 \x01(\tB\x03\xe0A\x02BG\n\x16com.exabel.api.data.v1B\x13SearchMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3', dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR])
_SEARCHTERM = _descriptor.Descriptor(name='SearchTerm', full_name='exabel.api.data.v1.SearchTerm', filename=None, file=DESCRIPTOR, containing_type=None, create_key=_descriptor._internal_create_key, fields=[_descriptor.FieldDescriptor(name='field', full_name='exabel.api.data.v1.SearchTerm.field', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=b''.decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=b'\xe0A\x02', file=DESCRIPTOR, create_key=_descriptor._internal_create_key), _descriptor.FieldDescriptor(name='query', full_name='exabel.api.data.v1.SearchTerm.query', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=b''.decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=b'\xe0A\x02', file=DESCRIPTOR, create_key=_descriptor._internal_create_key)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=97, serialized_end=149)
DESCRIPTOR.message_types_by_name['SearchTerm'] = _SEARCHTERM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
SearchTerm = _reflection.GeneratedProtocolMessageType('SearchTerm', (_message.Message,), {'DESCRIPTOR': _SEARCHTERM, '__module__': 'exabel.api.data.v1.search_messages_pb2'})
_sym_db.RegisterMessage(SearchTerm)
DESCRIPTOR._options = None
_SEARCHTERM.fields_by_name['field']._options = None
_SEARCHTERM.fields_by_name['query']._options = None