"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2
from ...protoc_gen_openapiv2.options import openapiv2_pb2 as protoc__gen__openapiv2_dot_options_dot_openapiv2__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.protoc_gen_openapiv2/options/annotations.proto\x12)grpc.gateway.protoc_gen_openapiv2.options\x1a google/protobuf/descriptor.proto\x1a,protoc_gen_openapiv2/options/openapiv2.proto:l\n\x11openapiv2_swagger\x12\x1c.google.protobuf.FileOptions\x18\x92\x08 \x01(\x0b22.grpc.gateway.protoc_gen_openapiv2.options.Swagger:r\n\x13openapiv2_operation\x12\x1e.google.protobuf.MethodOptions\x18\x92\x08 \x01(\x0b24.grpc.gateway.protoc_gen_openapiv2.options.Operation:m\n\x10openapiv2_schema\x12\x1f.google.protobuf.MessageOptions\x18\x92\x08 \x01(\x0b21.grpc.gateway.protoc_gen_openapiv2.options.Schema:g\n\ropenapiv2_tag\x12\x1f.google.protobuf.ServiceOptions\x18\x92\x08 \x01(\x0b2..grpc.gateway.protoc_gen_openapiv2.options.Tag:n\n\x0fopenapiv2_field\x12\x1d.google.protobuf.FieldOptions\x18\x92\x08 \x01(\x0b25.grpc.gateway.protoc_gen_openapiv2.options.JSONSchemaBHZFgithub.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2/optionsb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protoc_gen_openapiv2.options.annotations_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    google_dot_protobuf_dot_descriptor__pb2.FileOptions.RegisterExtension(openapiv2_swagger)
    google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(openapiv2_operation)
    google_dot_protobuf_dot_descriptor__pb2.MessageOptions.RegisterExtension(openapiv2_schema)
    google_dot_protobuf_dot_descriptor__pb2.ServiceOptions.RegisterExtension(openapiv2_tag)
    google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(openapiv2_field)
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZFgithub.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2/options'