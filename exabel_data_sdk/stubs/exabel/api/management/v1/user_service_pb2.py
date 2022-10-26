"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....exabel.api.management.v1 import user_messages_pb2 as exabel_dot_api_dot_management_dot_v1_dot_user__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+exabel/api/management/v1/user_service.proto\x12\x18exabel.api.management.v1\x1a,exabel/api/management/v1/user_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x13\n\x11ListGroupsRequest"E\n\x12ListGroupsResponse\x12/\n\x06groups\x18\x01 \x03(\x0b2\x1f.exabel.api.management.v1.Group"\x12\n\x10ListUsersRequest"B\n\x11ListUsersResponse\x12-\n\x05users\x18\x01 \x03(\x0b2\x1e.exabel.api.management.v1.User2\xa4\x02\n\x0bUserService\x12\x8b\x01\n\nListGroups\x12+.exabel.api.management.v1.ListGroupsRequest\x1a,.exabel.api.management.v1.ListGroupsResponse""\x82\xd3\xe4\x93\x02\x0c\x12\n/v1/groups\x92A\r\x12\x0bList groups\x12\x86\x01\n\tListUsers\x12*.exabel.api.management.v1.ListUsersRequest\x1a+.exabel.api.management.v1.ListUsersResponse" \x82\xd3\xe4\x93\x02\x0b\x12\t/v1/users\x92A\x0c\x12\nList usersBP\n\x1ccom.exabel.api.management.v1B\x10UserServiceProtoP\x01Z\x1cexabel.com/api/management/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.management.v1.user_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x1ccom.exabel.api.management.v1B\x10UserServiceProtoP\x01Z\x1cexabel.com/api/management/v1'
    _USERSERVICE.methods_by_name['ListGroups']._options = None
    _USERSERVICE.methods_by_name['ListGroups']._serialized_options = b'\x82\xd3\xe4\x93\x02\x0c\x12\n/v1/groups\x92A\r\x12\x0bList groups'
    _USERSERVICE.methods_by_name['ListUsers']._options = None
    _USERSERVICE.methods_by_name['ListUsers']._serialized_options = b'\x82\xd3\xe4\x93\x02\x0b\x12\t/v1/users\x92A\x0c\x12\nList users'
    _LISTGROUPSREQUEST._serialized_start = 197
    _LISTGROUPSREQUEST._serialized_end = 216
    _LISTGROUPSRESPONSE._serialized_start = 218
    _LISTGROUPSRESPONSE._serialized_end = 287
    _LISTUSERSREQUEST._serialized_start = 289
    _LISTUSERSREQUEST._serialized_end = 307
    _LISTUSERSRESPONSE._serialized_start = 309
    _LISTUSERSRESPONSE._serialized_end = 375
    _USERSERVICE._serialized_start = 378
    _USERSERVICE._serialized_end = 670