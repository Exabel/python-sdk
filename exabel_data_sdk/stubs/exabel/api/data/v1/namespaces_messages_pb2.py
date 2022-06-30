"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='exabel/api/data/v1/namespaces_messages.proto', package='exabel.api.data.v1', syntax='proto3', serialized_options=b'\n\x16com.exabel.api.data.v1B\x17NamespacesMessagesProtoP\x01Z\x16exabel.com/api/data/v1', create_key=_descriptor._internal_create_key, serialized_pb=b'\n,exabel/api/data/v1/namespaces_messages.proto\x12\x12exabel.api.data.v1\x1a\x1fgoogle/api/field_behavior.proto"6\n\tNamespace\x12\x11\n\x04name\x18\x01 \x01(\tB\x03\xe0A\x03\x12\x16\n\twriteable\x18\x02 \x01(\x08B\x03\xe0A\x03BK\n\x16com.exabel.api.data.v1B\x17NamespacesMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3', dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR])
_NAMESPACE = _descriptor.Descriptor(name='Namespace', full_name='exabel.api.data.v1.Namespace', filename=None, file=DESCRIPTOR, containing_type=None, create_key=_descriptor._internal_create_key, fields=[_descriptor.FieldDescriptor(name='name', full_name='exabel.api.data.v1.Namespace.name', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=b''.decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=b'\xe0A\x03', file=DESCRIPTOR, create_key=_descriptor._internal_create_key), _descriptor.FieldDescriptor(name='writeable', full_name='exabel.api.data.v1.Namespace.writeable', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=b'\xe0A\x03', file=DESCRIPTOR, create_key=_descriptor._internal_create_key)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=101, serialized_end=155)
DESCRIPTOR.message_types_by_name['Namespace'] = _NAMESPACE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
Namespace = _reflection.GeneratedProtocolMessageType('Namespace', (_message.Message,), {'DESCRIPTOR': _NAMESPACE, '__module__': 'exabel.api.data.v1.namespaces_messages_pb2'})
_sym_db.RegisterMessage(Namespace)
DESCRIPTOR._options = None
_NAMESPACE.fields_by_name['name']._options = None
_NAMESPACE.fields_by_name['writeable']._options = None