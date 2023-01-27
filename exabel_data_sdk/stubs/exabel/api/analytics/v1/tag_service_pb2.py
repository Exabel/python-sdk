"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....exabel.api.analytics.v1 import tag_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)exabel/api/analytics/v1/tag_service.proto\x12\x17exabel.api.analytics.v1\x1a*exabel/api/analytics/v1/tag_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"R\n\x10CreateTagRequest\x12.\n\x03tag\x18\x01 \x01(\x0b2\x1c.exabel.api.analytics.v1.TagB\x03\xe0A\x02\x12\x0e\n\x06folder\x18\x02 \x01(\t"2\n\rGetTagRequest\x12!\n\x04name\x18\x01 \x01(\tB\x13\xe0A\x02\x92A\r\xca>\n\xfa\x02\x07tagName"s\n\x10UpdateTagRequest\x12.\n\x03tag\x18\x01 \x01(\x0b2\x1c.exabel.api.analytics.v1.TagB\x03\xe0A\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask"5\n\x10DeleteTagRequest\x12!\n\x04name\x18\x01 \x01(\tB\x13\xe0A\x02\x92A\r\xca>\n\xfa\x02\x07tagName"8\n\x0fListTagsRequest\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12\x12\n\npage_token\x18\x02 \x01(\t"k\n\x10ListTagsResponse\x12*\n\x04tags\x18\x01 \x03(\x0b2\x1c.exabel.api.analytics.v1.Tag\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"M\n\x12AddEntitiesRequest\x12!\n\x04name\x18\x01 \x01(\tB\x13\xe0A\x02\x92A\r\xca>\n\xfa\x02\x07tagName\x12\x14\n\x0centity_names\x18\x02 \x03(\t"\x15\n\x13AddEntitiesResponse"P\n\x15RemoveEntitiesRequest\x12!\n\x04name\x18\x01 \x01(\tB\x13\xe0A\x02\x92A\r\xca>\n\xfa\x02\x07tagName\x12\x14\n\x0centity_names\x18\x02 \x03(\t"\x18\n\x16RemoveEntitiesResponse"d\n\x16ListTagEntitiesRequest\x12#\n\x06parent\x18\x01 \x01(\tB\x13\xe0A\x02\x92A\r\xca>\n\xfa\x02\x07tagName\x12\x11\n\tpage_size\x18\x02 \x01(\x05\x12\x12\n\npage_token\x18\x03 \x01(\t"\\\n\x17ListTagEntitiesResponse\x12\x14\n\x0centity_names\x18\x01 \x03(\t\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x052\xa5\t\n\nTagService\x12z\n\tCreateTag\x12).exabel.api.analytics.v1.CreateTagRequest\x1a\x1c.exabel.api.analytics.v1.Tag"$\x82\xd3\xe4\x93\x02\x0f"\x08/v1/tags:\x03tag\x92A\x0c\x12\nCreate tag\x12u\n\x06GetTag\x12&.exabel.api.analytics.v1.GetTagRequest\x1a\x1c.exabel.api.analytics.v1.Tag"%\x82\xd3\xe4\x93\x02\x13\x12\x11/v1/{name=tags/*}\x92A\t\x12\x07Get tag\x12\x87\x01\n\tUpdateTag\x12).exabel.api.analytics.v1.UpdateTagRequest\x1a\x1c.exabel.api.analytics.v1.Tag"1\x82\xd3\xe4\x93\x02\x1c2\x15/v1/{tag.name=tags/*}:\x03tag\x92A\x0c\x12\nUpdate tag\x12x\n\tDeleteTag\x12).exabel.api.analytics.v1.DeleteTagRequest\x1a\x16.google.protobuf.Empty"(\x82\xd3\xe4\x93\x02\x13*\x11/v1/{name=tags/*}\x92A\x0c\x12\nDelete tag\x12\x7f\n\x08ListTags\x12(.exabel.api.analytics.v1.ListTagsRequest\x1a).exabel.api.analytics.v1.ListTagsResponse"\x1e\x82\xd3\xe4\x93\x02\n\x12\x08/v1/tags\x92A\x0b\x12\tList tags\x12\xaa\x01\n\x0bAddEntities\x12+.exabel.api.analytics.v1.AddEntitiesRequest\x1a,.exabel.api.analytics.v1.AddEntitiesResponse"@\x82\xd3\xe4\x93\x02""\x1d/v1/{name=tags/*}:addEntities:\x01*\x92A\x15\x12\x13Add entities to tag\x12\xbb\x01\n\x0eRemoveEntities\x12..exabel.api.analytics.v1.RemoveEntitiesRequest\x1a/.exabel.api.analytics.v1.RemoveEntitiesResponse"H\x82\xd3\xe4\x93\x02%" /v1/{name=tags/*}:removeEntities:\x01*\x92A\x1a\x12\x18Remove entities from tag\x12\xb3\x01\n\x0fListTagEntities\x12/.exabel.api.analytics.v1.ListTagEntitiesRequest\x1a0.exabel.api.analytics.v1.ListTagEntitiesResponse"=\x82\xd3\xe4\x93\x02\x1e\x12\x1c/v1/{parent=tags/*}/entities\x92A\x16\x12\x14List entities in tagBM\n\x1bcom.exabel.api.analytics.v1B\x0fTagServiceProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.tag_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x0fTagServiceProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _CREATETAGREQUEST.fields_by_name['tag']._options = None
    _CREATETAGREQUEST.fields_by_name['tag']._serialized_options = b'\xe0A\x02'
    _GETTAGREQUEST.fields_by_name['name']._options = None
    _GETTAGREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\r\xca>\n\xfa\x02\x07tagName'
    _UPDATETAGREQUEST.fields_by_name['tag']._options = None
    _UPDATETAGREQUEST.fields_by_name['tag']._serialized_options = b'\xe0A\x02'
    _DELETETAGREQUEST.fields_by_name['name']._options = None
    _DELETETAGREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\r\xca>\n\xfa\x02\x07tagName'
    _ADDENTITIESREQUEST.fields_by_name['name']._options = None
    _ADDENTITIESREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\r\xca>\n\xfa\x02\x07tagName'
    _REMOVEENTITIESREQUEST.fields_by_name['name']._options = None
    _REMOVEENTITIESREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\r\xca>\n\xfa\x02\x07tagName'
    _LISTTAGENTITIESREQUEST.fields_by_name['parent']._options = None
    _LISTTAGENTITIESREQUEST.fields_by_name['parent']._serialized_options = b'\xe0A\x02\x92A\r\xca>\n\xfa\x02\x07tagName'
    _TAGSERVICE.methods_by_name['CreateTag']._options = None
    _TAGSERVICE.methods_by_name['CreateTag']._serialized_options = b'\x82\xd3\xe4\x93\x02\x0f"\x08/v1/tags:\x03tag\x92A\x0c\x12\nCreate tag'
    _TAGSERVICE.methods_by_name['GetTag']._options = None
    _TAGSERVICE.methods_by_name['GetTag']._serialized_options = b'\x82\xd3\xe4\x93\x02\x13\x12\x11/v1/{name=tags/*}\x92A\t\x12\x07Get tag'
    _TAGSERVICE.methods_by_name['UpdateTag']._options = None
    _TAGSERVICE.methods_by_name['UpdateTag']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1c2\x15/v1/{tag.name=tags/*}:\x03tag\x92A\x0c\x12\nUpdate tag'
    _TAGSERVICE.methods_by_name['DeleteTag']._options = None
    _TAGSERVICE.methods_by_name['DeleteTag']._serialized_options = b'\x82\xd3\xe4\x93\x02\x13*\x11/v1/{name=tags/*}\x92A\x0c\x12\nDelete tag'
    _TAGSERVICE.methods_by_name['ListTags']._options = None
    _TAGSERVICE.methods_by_name['ListTags']._serialized_options = b'\x82\xd3\xe4\x93\x02\n\x12\x08/v1/tags\x92A\x0b\x12\tList tags'
    _TAGSERVICE.methods_by_name['AddEntities']._options = None
    _TAGSERVICE.methods_by_name['AddEntities']._serialized_options = b'\x82\xd3\xe4\x93\x02""\x1d/v1/{name=tags/*}:addEntities:\x01*\x92A\x15\x12\x13Add entities to tag'
    _TAGSERVICE.methods_by_name['RemoveEntities']._options = None
    _TAGSERVICE.methods_by_name['RemoveEntities']._serialized_options = b'\x82\xd3\xe4\x93\x02%" /v1/{name=tags/*}:removeEntities:\x01*\x92A\x1a\x12\x18Remove entities from tag'
    _TAGSERVICE.methods_by_name['ListTagEntities']._options = None
    _TAGSERVICE.methods_by_name['ListTagEntities']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1e\x12\x1c/v1/{parent=tags/*}/entities\x92A\x16\x12\x14List entities in tag'
    _CREATETAGREQUEST._serialized_start = 288
    _CREATETAGREQUEST._serialized_end = 370
    _GETTAGREQUEST._serialized_start = 372
    _GETTAGREQUEST._serialized_end = 422
    _UPDATETAGREQUEST._serialized_start = 424
    _UPDATETAGREQUEST._serialized_end = 539
    _DELETETAGREQUEST._serialized_start = 541
    _DELETETAGREQUEST._serialized_end = 594
    _LISTTAGSREQUEST._serialized_start = 596
    _LISTTAGSREQUEST._serialized_end = 652
    _LISTTAGSRESPONSE._serialized_start = 654
    _LISTTAGSRESPONSE._serialized_end = 761
    _ADDENTITIESREQUEST._serialized_start = 763
    _ADDENTITIESREQUEST._serialized_end = 840
    _ADDENTITIESRESPONSE._serialized_start = 842
    _ADDENTITIESRESPONSE._serialized_end = 863
    _REMOVEENTITIESREQUEST._serialized_start = 865
    _REMOVEENTITIESREQUEST._serialized_end = 945
    _REMOVEENTITIESRESPONSE._serialized_start = 947
    _REMOVEENTITIESRESPONSE._serialized_end = 971
    _LISTTAGENTITIESREQUEST._serialized_start = 973
    _LISTTAGENTITIESREQUEST._serialized_end = 1073
    _LISTTAGENTITIESRESPONSE._serialized_start = 1075
    _LISTTAGENTITIESRESPONSE._serialized_end = 1167
    _TAGSERVICE._serialized_start = 1170
    _TAGSERVICE._serialized_end = 2359