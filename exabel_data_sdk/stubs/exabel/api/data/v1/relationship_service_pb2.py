"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....exabel.api.data.v1 import relationship_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-exabel/api/data/v1/relationship_service.proto\x12\x12exabel.api.data.v1\x1a.exabel/api/data/v1/relationship_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"E\n\x1cListRelationshipTypesRequest\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12\x12\n\npage_token\x18\x02 \x01(\t"\x8e\x01\n\x1dListRelationshipTypesResponse\x12@\n\x12relationship_types\x18\x01 \x03(\x0b2$.exabel.api.data.v1.RelationshipType\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"e\n\x1dCreateRelationshipTypeRequest\x12D\n\x11relationship_type\x18\x01 \x01(\x0b2$.exabel.api.data.v1.RelationshipTypeB\x03\xe0A\x02"\xad\x01\n\x1dUpdateRelationshipTypeRequest\x12D\n\x11relationship_type\x18\x01 \x01(\x0b2$.exabel.api.data.v1.RelationshipTypeB\x03\xe0A\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask\x12\x15\n\rallow_missing\x18\x03 \x01(\x08"O\n\x1dDeleteRelationshipTypeRequest\x12.\n\x04name\x18\x01 \x01(\tB \xe0A\x02\x92A\x1a\xca>\x17\xfa\x02\x14relationshipTypeName"L\n\x1aGetRelationshipTypeRequest\x12.\n\x04name\x18\x01 \x01(\tB \xe0A\x02\x92A\x1a\xca>\x17\xfa\x02\x14relationshipTypeName"\x9b\x01\n\x18ListRelationshipsRequest\x120\n\x06parent\x18\x01 \x01(\tB \xe0A\x02\x92A\x1a\xca>\x17\xfa\x02\x14relationshipTypeName\x12\x13\n\x0bfrom_entity\x18\x02 \x01(\t\x12\x11\n\tto_entity\x18\x03 \x01(\t\x12\x11\n\tpage_size\x18\x04 \x01(\x05\x12\x12\n\npage_token\x18\x05 \x01(\t"\x81\x01\n\x19ListRelationshipsResponse\x127\n\rrelationships\x18\x01 \x03(\x0b2 .exabel.api.data.v1.Relationship\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"|\n\x16GetRelationshipRequest\x120\n\x06parent\x18\x01 \x01(\tB \xe0A\x02\x92A\x1a\xca>\x17\xfa\x02\x14relationshipTypeName\x12\x18\n\x0bfrom_entity\x18\x02 \x01(\tB\x03\xe0A\x02\x12\x16\n\tto_entity\x18\x03 \x01(\tB\x03\xe0A\x02"X\n\x19CreateRelationshipRequest\x12;\n\x0crelationship\x18\x01 \x01(\x0b2 .exabel.api.data.v1.RelationshipB\x03\xe0A\x02"\xa0\x01\n\x19UpdateRelationshipRequest\x12;\n\x0crelationship\x18\x01 \x01(\x0b2 .exabel.api.data.v1.RelationshipB\x03\xe0A\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask\x12\x15\n\rallow_missing\x18\x03 \x01(\x08"\x7f\n\x19DeleteRelationshipRequest\x120\n\x06parent\x18\x01 \x01(\tB \xe0A\x02\x92A\x1a\xca>\x17\xfa\x02\x14relationshipTypeName\x12\x18\n\x0bfrom_entity\x18\x02 \x01(\tB\x03\xe0A\x02\x12\x16\n\tto_entity\x18\x03 \x01(\tB\x03\xe0A\x022\x94\x12\n\x13RelationshipService\x12\xb7\x01\n\x15ListRelationshipTypes\x120.exabel.api.data.v1.ListRelationshipTypesRequest\x1a1.exabel.api.data.v1.ListRelationshipTypesResponse"9\x82\xd3\xe4\x93\x02\x17\x12\x15/v1/relationshipTypes\x92A\x19\x12\x17List relationship types\x12\xad\x01\n\x13GetRelationshipType\x12..exabel.api.data.v1.GetRelationshipTypeRequest\x1a$.exabel.api.data.v1.RelationshipType"@\x82\xd3\xe4\x93\x02 \x12\x1e/v1/{name=relationshipTypes/*}\x92A\x17\x12\x15Get relationship type\x12\xc0\x01\n\x16CreateRelationshipType\x121.exabel.api.data.v1.CreateRelationshipTypeRequest\x1a$.exabel.api.data.v1.RelationshipType"M\x82\xd3\xe4\x93\x02*"\x15/v1/relationshipTypes:\x11relationship_type\x92A\x1a\x12\x18Create relationship type\x12\xdb\x01\n\x16UpdateRelationshipType\x121.exabel.api.data.v1.UpdateRelationshipTypeRequest\x1a$.exabel.api.data.v1.RelationshipType"h\x82\xd3\xe4\x93\x02E20/v1/{relationship_type.name=relationshipTypes/*}:\x11relationship_type\x92A\x1a\x12\x18Update relationship type\x12\xa8\x01\n\x16DeleteRelationshipType\x121.exabel.api.data.v1.DeleteRelationshipTypeRequest\x1a\x16.google.protobuf.Empty"C\x82\xd3\xe4\x93\x02 *\x1e/v1/{name=relationshipTypes/*}\x92A\x1a\x12\x18Delete relationship type\x12\xbf\x01\n\x11ListRelationships\x12,.exabel.api.data.v1.ListRelationshipsRequest\x1a-.exabel.api.data.v1.ListRelationshipsResponse"M\x82\xd3\xe4\x93\x020\x12./v1/{parent=relationshipTypes/*}/relationships\x92A\x14\x12\x12List relationships\x12\xf9\x01\n\x0fGetRelationship\x12*.exabel.api.data.v1.GetRelationshipRequest\x1a .exabel.api.data.v1.Relationship"\x97\x01\x82\xd3\xe4\x93\x02|\x12z/v1/{parent=relationshipTypes/*}/relationships/{from_entity=entityTypes/*/entities/*}/{to_entity=entityTypes/*/entities/*}\x92A\x12\x12\x10Get relationship\x12\xd0\x01\n\x12CreateRelationship\x12-.exabel.api.data.v1.CreateRelationshipRequest\x1a .exabel.api.data.v1.Relationship"i\x82\xd3\xe4\x93\x02K";/v1/{relationship.parent=relationshipTypes/*}/relationships:\x0crelationship\x92A\x15\x12\x13Create relationship\x12\x87\x03\n\x12UpdateRelationship\x12-.exabel.api.data.v1.UpdateRelationshipRequest\x1a .exabel.api.data.v1.Relationship"\x9f\x02\x82\xd3\xe4\x93\x02\x80\x022;/v1/{relationship.parent=relationshipTypes/*}/relationships:\x0crelationshipZ\xb2\x012\xa1\x01/v1/{relationship.parent=relationshipTypes/*}/relationships/{relationship.from_entity=entityTypes/*/entities/*}/{relationship.to_entity=entityTypes/*/entities/*}:\x0crelationship\x92A\x15\x12\x13Update relationship\x12\xab\x02\n\x12DeleteRelationship\x12-.exabel.api.data.v1.DeleteRelationshipRequest\x1a\x16.google.protobuf.Empty"\xcd\x01\x82\xd3\xe4\x93\x02\xae\x01*./v1/{parent=relationshipTypes/*}/relationshipsZ|*z/v1/{parent=relationshipTypes/*}/relationships/{from_entity=entityTypes/*/entities/*}/{to_entity=entityTypes/*/entities/*}\x92A\x15\x12\x13Delete relationshipBL\n\x16com.exabel.api.data.v1B\x18RelationshipServiceProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.relationship_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x18RelationshipServiceProtoP\x01Z\x16exabel.com/api/data/v1'
    _CREATERELATIONSHIPTYPEREQUEST.fields_by_name['relationship_type']._options = None
    _CREATERELATIONSHIPTYPEREQUEST.fields_by_name['relationship_type']._serialized_options = b'\xe0A\x02'
    _UPDATERELATIONSHIPTYPEREQUEST.fields_by_name['relationship_type']._options = None
    _UPDATERELATIONSHIPTYPEREQUEST.fields_by_name['relationship_type']._serialized_options = b'\xe0A\x02'
    _DELETERELATIONSHIPTYPEREQUEST.fields_by_name['name']._options = None
    _DELETERELATIONSHIPTYPEREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\x1a\xca>\x17\xfa\x02\x14relationshipTypeName'
    _GETRELATIONSHIPTYPEREQUEST.fields_by_name['name']._options = None
    _GETRELATIONSHIPTYPEREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\x1a\xca>\x17\xfa\x02\x14relationshipTypeName'
    _LISTRELATIONSHIPSREQUEST.fields_by_name['parent']._options = None
    _LISTRELATIONSHIPSREQUEST.fields_by_name['parent']._serialized_options = b'\xe0A\x02\x92A\x1a\xca>\x17\xfa\x02\x14relationshipTypeName'
    _GETRELATIONSHIPREQUEST.fields_by_name['parent']._options = None
    _GETRELATIONSHIPREQUEST.fields_by_name['parent']._serialized_options = b'\xe0A\x02\x92A\x1a\xca>\x17\xfa\x02\x14relationshipTypeName'
    _GETRELATIONSHIPREQUEST.fields_by_name['from_entity']._options = None
    _GETRELATIONSHIPREQUEST.fields_by_name['from_entity']._serialized_options = b'\xe0A\x02'
    _GETRELATIONSHIPREQUEST.fields_by_name['to_entity']._options = None
    _GETRELATIONSHIPREQUEST.fields_by_name['to_entity']._serialized_options = b'\xe0A\x02'
    _CREATERELATIONSHIPREQUEST.fields_by_name['relationship']._options = None
    _CREATERELATIONSHIPREQUEST.fields_by_name['relationship']._serialized_options = b'\xe0A\x02'
    _UPDATERELATIONSHIPREQUEST.fields_by_name['relationship']._options = None
    _UPDATERELATIONSHIPREQUEST.fields_by_name['relationship']._serialized_options = b'\xe0A\x02'
    _DELETERELATIONSHIPREQUEST.fields_by_name['parent']._options = None
    _DELETERELATIONSHIPREQUEST.fields_by_name['parent']._serialized_options = b'\xe0A\x02\x92A\x1a\xca>\x17\xfa\x02\x14relationshipTypeName'
    _DELETERELATIONSHIPREQUEST.fields_by_name['from_entity']._options = None
    _DELETERELATIONSHIPREQUEST.fields_by_name['from_entity']._serialized_options = b'\xe0A\x02'
    _DELETERELATIONSHIPREQUEST.fields_by_name['to_entity']._options = None
    _DELETERELATIONSHIPREQUEST.fields_by_name['to_entity']._serialized_options = b'\xe0A\x02'
    _RELATIONSHIPSERVICE.methods_by_name['ListRelationshipTypes']._options = None
    _RELATIONSHIPSERVICE.methods_by_name['ListRelationshipTypes']._serialized_options = b'\x82\xd3\xe4\x93\x02\x17\x12\x15/v1/relationshipTypes\x92A\x19\x12\x17List relationship types'
    _RELATIONSHIPSERVICE.methods_by_name['GetRelationshipType']._options = None
    _RELATIONSHIPSERVICE.methods_by_name['GetRelationshipType']._serialized_options = b'\x82\xd3\xe4\x93\x02 \x12\x1e/v1/{name=relationshipTypes/*}\x92A\x17\x12\x15Get relationship type'
    _RELATIONSHIPSERVICE.methods_by_name['CreateRelationshipType']._options = None
    _RELATIONSHIPSERVICE.methods_by_name['CreateRelationshipType']._serialized_options = b'\x82\xd3\xe4\x93\x02*"\x15/v1/relationshipTypes:\x11relationship_type\x92A\x1a\x12\x18Create relationship type'
    _RELATIONSHIPSERVICE.methods_by_name['UpdateRelationshipType']._options = None
    _RELATIONSHIPSERVICE.methods_by_name['UpdateRelationshipType']._serialized_options = b'\x82\xd3\xe4\x93\x02E20/v1/{relationship_type.name=relationshipTypes/*}:\x11relationship_type\x92A\x1a\x12\x18Update relationship type'
    _RELATIONSHIPSERVICE.methods_by_name['DeleteRelationshipType']._options = None
    _RELATIONSHIPSERVICE.methods_by_name['DeleteRelationshipType']._serialized_options = b'\x82\xd3\xe4\x93\x02 *\x1e/v1/{name=relationshipTypes/*}\x92A\x1a\x12\x18Delete relationship type'
    _RELATIONSHIPSERVICE.methods_by_name['ListRelationships']._options = None
    _RELATIONSHIPSERVICE.methods_by_name['ListRelationships']._serialized_options = b'\x82\xd3\xe4\x93\x020\x12./v1/{parent=relationshipTypes/*}/relationships\x92A\x14\x12\x12List relationships'
    _RELATIONSHIPSERVICE.methods_by_name['GetRelationship']._options = None
    _RELATIONSHIPSERVICE.methods_by_name['GetRelationship']._serialized_options = b'\x82\xd3\xe4\x93\x02|\x12z/v1/{parent=relationshipTypes/*}/relationships/{from_entity=entityTypes/*/entities/*}/{to_entity=entityTypes/*/entities/*}\x92A\x12\x12\x10Get relationship'
    _RELATIONSHIPSERVICE.methods_by_name['CreateRelationship']._options = None
    _RELATIONSHIPSERVICE.methods_by_name['CreateRelationship']._serialized_options = b'\x82\xd3\xe4\x93\x02K";/v1/{relationship.parent=relationshipTypes/*}/relationships:\x0crelationship\x92A\x15\x12\x13Create relationship'
    _RELATIONSHIPSERVICE.methods_by_name['UpdateRelationship']._options = None
    _RELATIONSHIPSERVICE.methods_by_name['UpdateRelationship']._serialized_options = b'\x82\xd3\xe4\x93\x02\x80\x022;/v1/{relationship.parent=relationshipTypes/*}/relationships:\x0crelationshipZ\xb2\x012\xa1\x01/v1/{relationship.parent=relationshipTypes/*}/relationships/{relationship.from_entity=entityTypes/*/entities/*}/{relationship.to_entity=entityTypes/*/entities/*}:\x0crelationship\x92A\x15\x12\x13Update relationship'
    _RELATIONSHIPSERVICE.methods_by_name['DeleteRelationship']._options = None
    _RELATIONSHIPSERVICE.methods_by_name['DeleteRelationship']._serialized_options = b'\x82\xd3\xe4\x93\x02\xae\x01*./v1/{parent=relationshipTypes/*}/relationshipsZ|*z/v1/{parent=relationshipTypes/*}/relationships/{from_entity=entityTypes/*/entities/*}/{to_entity=entityTypes/*/entities/*}\x92A\x15\x12\x13Delete relationship'
    _LISTRELATIONSHIPTYPESREQUEST._serialized_start = 291
    _LISTRELATIONSHIPTYPESREQUEST._serialized_end = 360
    _LISTRELATIONSHIPTYPESRESPONSE._serialized_start = 363
    _LISTRELATIONSHIPTYPESRESPONSE._serialized_end = 505
    _CREATERELATIONSHIPTYPEREQUEST._serialized_start = 507
    _CREATERELATIONSHIPTYPEREQUEST._serialized_end = 608
    _UPDATERELATIONSHIPTYPEREQUEST._serialized_start = 611
    _UPDATERELATIONSHIPTYPEREQUEST._serialized_end = 784
    _DELETERELATIONSHIPTYPEREQUEST._serialized_start = 786
    _DELETERELATIONSHIPTYPEREQUEST._serialized_end = 865
    _GETRELATIONSHIPTYPEREQUEST._serialized_start = 867
    _GETRELATIONSHIPTYPEREQUEST._serialized_end = 943
    _LISTRELATIONSHIPSREQUEST._serialized_start = 946
    _LISTRELATIONSHIPSREQUEST._serialized_end = 1101
    _LISTRELATIONSHIPSRESPONSE._serialized_start = 1104
    _LISTRELATIONSHIPSRESPONSE._serialized_end = 1233
    _GETRELATIONSHIPREQUEST._serialized_start = 1235
    _GETRELATIONSHIPREQUEST._serialized_end = 1359
    _CREATERELATIONSHIPREQUEST._serialized_start = 1361
    _CREATERELATIONSHIPREQUEST._serialized_end = 1449
    _UPDATERELATIONSHIPREQUEST._serialized_start = 1452
    _UPDATERELATIONSHIPREQUEST._serialized_end = 1612
    _DELETERELATIONSHIPREQUEST._serialized_start = 1614
    _DELETERELATIONSHIPREQUEST._serialized_end = 1741
    _RELATIONSHIPSERVICE._serialized_start = 1744
    _RELATIONSHIPSERVICE._serialized_end = 4068