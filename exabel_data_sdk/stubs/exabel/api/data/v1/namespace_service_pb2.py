"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/data/v1/namespace_service.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.data.v1 import namespaces_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_namespaces__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*exabel/api/data/v1/namespace_service.proto\x12\x12exabel.api.data.v1\x1a,exabel/api/data/v1/namespaces_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x17\n\x15ListNamespacesRequest"K\n\x16ListNamespacesResponse\x121\n\nnamespaces\x18\x01 \x03(\x0b2\x1d.exabel.api.data.v1.Namespace2\xa8\x01\n\x10NamespaceService\x12\x93\x01\n\x0eListNamespaces\x12).exabel.api.data.v1.ListNamespacesRequest\x1a*.exabel.api.data.v1.ListNamespacesResponse"*\x92A\x11\x12\x0fList namespaces\x82\xd3\xe4\x93\x02\x10\x12\x0e/v1/namespacesBI\n\x16com.exabel.api.data.v1B\x15NamespaceServiceProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.namespace_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x15NamespaceServiceProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_NAMESPACESERVICE'].methods_by_name['ListNamespaces']._loaded_options = None
    _globals['_NAMESPACESERVICE'].methods_by_name['ListNamespaces']._serialized_options = b'\x92A\x11\x12\x0fList namespaces\x82\xd3\xe4\x93\x02\x10\x12\x0e/v1/namespaces'
    _globals['_LISTNAMESPACESREQUEST']._serialized_start = 190
    _globals['_LISTNAMESPACESREQUEST']._serialized_end = 213
    _globals['_LISTNAMESPACESRESPONSE']._serialized_start = 215
    _globals['_LISTNAMESPACESRESPONSE']._serialized_end = 290
    _globals['_NAMESPACESERVICE']._serialized_start = 293
    _globals['_NAMESPACESERVICE']._serialized_end = 461