"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+exabel/api/data/v1/import_job_service.proto\x12\x12exabel.api.data.v1\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"4\n\x0eRunTaskRequest\x12"\n\x04name\x18\x01 \x01(\tB\x14\xe0A\x02\x92A\x0e\xca>\x0b\xfa\x02\x08taskName"\x11\n\x0fRunTaskResponse2\x9e\x01\n\x10ImportJobService\x12\x89\x01\n\x07RunTask\x12".exabel.api.data.v1.RunTaskRequest\x1a#.exabel.api.data.v1.RunTaskResponse"5\x82\xd3\xe4\x93\x02\x1b"\x16/v1/{name=tasks/*}:run:\x01*\x92A\x11\x12\x0fRun import taskBJ\n\x16com.exabel.api.data.v1B\x16ImportJobsServiceProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.import_job_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x16ImportJobsServiceProtoP\x01Z\x16exabel.com/api/data/v1'
    _RUNTASKREQUEST.fields_by_name['name']._options = None
    _RUNTASKREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\x0e\xca>\x0b\xfa\x02\x08taskName'
    _IMPORTJOBSERVICE.methods_by_name['RunTask']._options = None
    _IMPORTJOBSERVICE.methods_by_name['RunTask']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1b"\x16/v1/{name=tasks/*}:run:\x01*\x92A\x11\x12\x0fRun import task'
    _RUNTASKREQUEST._serialized_start = 178
    _RUNTASKREQUEST._serialized_end = 230
    _RUNTASKRESPONSE._serialized_start = 232
    _RUNTASKRESPONSE._serialized_end = 249
    _IMPORTJOBSERVICE._serialized_start = 252
    _IMPORTJOBSERVICE._serialized_end = 410