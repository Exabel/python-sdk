"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/data/v1/entity_service.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.data.v1 import entity_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2
from .....exabel.api.data.v1 import search_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_search__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'exabel/api/data/v1/entity_service.proto\x12\x12exabel.api.data.v1\x1a(exabel/api/data/v1/entity_messages.proto\x1a(exabel/api/data/v1/search_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"?\n\x16ListEntityTypesRequest\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12\x12\n\npage_token\x18\x02 \x01(\t"|\n\x17ListEntityTypesResponse\x124\n\x0centity_types\x18\x01 \x03(\x0b2\x1e.exabel.api.data.v1.EntityType\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"@\n\x14GetEntityTypeRequest\x12(\n\x04name\x18\x01 \x01(\tB\x1a\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02"j\n\x17CreateEntityTypeRequest\x12O\n\x0bentity_type\x18\x01 \x01(\x0b2\x1e.exabel.api.data.v1.EntityTypeB\x1a\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02"\xb2\x01\n\x17UpdateEntityTypeRequest\x12O\n\x0bentity_type\x18\x01 \x01(\x0b2\x1e.exabel.api.data.v1.EntityTypeB\x1a\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask\x12\x15\n\rallow_missing\x18\x03 \x01(\x08"C\n\x17DeleteEntityTypeRequest\x12(\n\x04name\x18\x01 \x01(\tB\x1a\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02"h\n\x13ListEntitiesRequest\x12*\n\x06parent\x18\x01 \x01(\tB\x1a\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02\x12\x11\n\tpage_size\x18\x02 \x01(\x05\x12\x12\n\npage_token\x18\x03 \x01(\t"q\n\x14ListEntitiesResponse\x12,\n\x08entities\x18\x01 \x03(\x0b2\x1a.exabel.api.data.v1.Entity\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"T\n\x15DeleteEntitiesRequest\x12*\n\x06parent\x18\x01 \x01(\tB\x1a\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02\x12\x0f\n\x07confirm\x18\x02 \x01(\x08"8\n\x10GetEntityRequest\x12$\n\x04name\x18\x01 \x01(\tB\x16\x92A\x10\xca>\r\xfa\x02\nentityName\xe0A\x02"r\n\x13CreateEntityRequest\x12*\n\x06parent\x18\x01 \x01(\tB\x1a\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02\x12/\n\x06entity\x18\x02 \x01(\x0b2\x1a.exabel.api.data.v1.EntityB\x03\xe0A\x02"\xa1\x01\n\x13UpdateEntityRequest\x12B\n\x06entity\x18\x01 \x01(\x0b2\x1a.exabel.api.data.v1.EntityB\x16\x92A\x10\xca>\r\xfa\x02\nentityName\xe0A\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask\x12\x15\n\rallow_missing\x18\x03 \x01(\x08";\n\x13DeleteEntityRequest\x12$\n\x04name\x18\x01 \x01(\tB\x16\x92A\x10\xca>\r\xfa\x02\nentityName\xe0A\x02"\xd2\x01\n\x15SearchEntitiesRequest\x12*\n\x06parent\x18\x04 \x01(\tB\x1a\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02\x122\n\x05terms\x18\x01 \x03(\x0b2\x1e.exabel.api.data.v1.SearchTermB\x03\xe0A\x02\x122\n\x07options\x18\x05 \x01(\x0b2!.exabel.api.data.v1.SearchOptions\x12\x11\n\tpage_size\x18\x02 \x01(\x05\x12\x12\n\npage_token\x18\x03 \x01(\t"\x96\x02\n\x16SearchEntitiesResponse\x12H\n\x07results\x18\x03 \x03(\x0b27.exabel.api.data.v1.SearchEntitiesResponse.SearchResult\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12,\n\x08entities\x18\x01 \x03(\x0b2\x1a.exabel.api.data.v1.Entity\x1ak\n\x0cSearchResult\x12-\n\x05terms\x18\x01 \x03(\x0b2\x1e.exabel.api.data.v1.SearchTerm\x12,\n\x08entities\x18\x02 \x03(\x0b2\x1a.exabel.api.data.v1.Entity2\xf7\x0e\n\rEntityService\x12\x99\x01\n\x0fListEntityTypes\x12*.exabel.api.data.v1.ListEntityTypesRequest\x1a+.exabel.api.data.v1.ListEntityTypesResponse"-\x92A\x13\x12\x11List entity types\x82\xd3\xe4\x93\x02\x11\x12\x0f/v1/entityTypes\x12\x8f\x01\n\rGetEntityType\x12(.exabel.api.data.v1.GetEntityTypeRequest\x1a\x1e.exabel.api.data.v1.EntityType"4\x92A\x11\x12\x0fGet entity type\x82\xd3\xe4\x93\x02\x1a\x12\x18/v1/{name=entityTypes/*}\x12\x9c\x01\n\x10CreateEntityType\x12+.exabel.api.data.v1.CreateEntityTypeRequest\x1a\x1e.exabel.api.data.v1.EntityType";\x92A\x14\x12\x12Create entity type\x82\xd3\xe4\x93\x02\x1e"\x0f/v1/entityTypes:\x0bentity_type\x12\xb1\x01\n\x10UpdateEntityType\x12+.exabel.api.data.v1.UpdateEntityTypeRequest\x1a\x1e.exabel.api.data.v1.EntityType"P\x92A\x14\x12\x12Update entity type\x82\xd3\xe4\x93\x0232$/v1/{entity_type.name=entityTypes/*}:\x0bentity_type\x12\x90\x01\n\x10DeleteEntityType\x12+.exabel.api.data.v1.DeleteEntityTypeRequest\x1a\x16.google.protobuf.Empty"7\x92A\x14\x12\x12Delete entity type\x82\xd3\xe4\x93\x02\x1a*\x18/v1/{name=entityTypes/*}\x12\xa0\x01\n\x0cListEntities\x12\'.exabel.api.data.v1.ListEntitiesRequest\x1a(.exabel.api.data.v1.ListEntitiesResponse"=\x92A\x0f\x12\rList entities\x82\xd3\xe4\x93\x02%\x12#/v1/{parent=entityTypes/*}/entities\x12\x9b\x01\n\x0eDeleteEntities\x12).exabel.api.data.v1.DeleteEntitiesRequest\x1a\x16.google.protobuf.Empty"F\x92A\x18\x12\x16Delete entities (bulk)\x82\xd3\xe4\x93\x02%*#/v1/{parent=entityTypes/*}/entities\x12\x89\x01\n\tGetEntity\x12$.exabel.api.data.v1.GetEntityRequest\x1a\x1a.exabel.api.data.v1.Entity":\x92A\x0c\x12\nGet entity\x82\xd3\xe4\x93\x02%\x12#/v1/{name=entityTypes/*/entities/*}\x12\x9a\x01\n\x0cCreateEntity\x12\'.exabel.api.data.v1.CreateEntityRequest\x1a\x1a.exabel.api.data.v1.Entity"E\x92A\x0f\x12\rCreate entity\x82\xd3\xe4\x93\x02-"#/v1/{parent=entityTypes/*}/entities:\x06entity\x12\xa1\x01\n\x0cUpdateEntity\x12\'.exabel.api.data.v1.UpdateEntityRequest\x1a\x1a.exabel.api.data.v1.Entity"L\x92A\x0f\x12\rUpdate entity\x82\xd3\xe4\x93\x0242*/v1/{entity.name=entityTypes/*/entities/*}:\x06entity\x12\x8e\x01\n\x0cDeleteEntity\x12\'.exabel.api.data.v1.DeleteEntityRequest\x1a\x16.google.protobuf.Empty"=\x92A\x0f\x12\rDelete entity\x82\xd3\xe4\x93\x02%*#/v1/{name=entityTypes/*/entities/*}\x12\xb2\x01\n\x0eSearchEntities\x12).exabel.api.data.v1.SearchEntitiesRequest\x1a*.exabel.api.data.v1.SearchEntitiesResponse"I\x92A\x11\x12\x0fSearch entities\x82\xd3\xe4\x93\x02/"*/v1/{parent=entityTypes/*}/entities:search:\x01*BF\n\x16com.exabel.api.data.v1B\x12EntityServiceProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.entity_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x12EntityServiceProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_GETENTITYTYPEREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_GETENTITYTYPEREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02'
    _globals['_CREATEENTITYTYPEREQUEST'].fields_by_name['entity_type']._loaded_options = None
    _globals['_CREATEENTITYTYPEREQUEST'].fields_by_name['entity_type']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02'
    _globals['_UPDATEENTITYTYPEREQUEST'].fields_by_name['entity_type']._loaded_options = None
    _globals['_UPDATEENTITYTYPEREQUEST'].fields_by_name['entity_type']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02'
    _globals['_DELETEENTITYTYPEREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_DELETEENTITYTYPEREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02'
    _globals['_LISTENTITIESREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_LISTENTITIESREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02'
    _globals['_DELETEENTITIESREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_DELETEENTITIESREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02'
    _globals['_GETENTITYREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_GETENTITYREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x10\xca>\r\xfa\x02\nentityName\xe0A\x02'
    _globals['_CREATEENTITYREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_CREATEENTITYREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02'
    _globals['_CREATEENTITYREQUEST'].fields_by_name['entity']._loaded_options = None
    _globals['_CREATEENTITYREQUEST'].fields_by_name['entity']._serialized_options = b'\xe0A\x02'
    _globals['_UPDATEENTITYREQUEST'].fields_by_name['entity']._loaded_options = None
    _globals['_UPDATEENTITYREQUEST'].fields_by_name['entity']._serialized_options = b'\x92A\x10\xca>\r\xfa\x02\nentityName\xe0A\x02'
    _globals['_DELETEENTITYREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_DELETEENTITYREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x10\xca>\r\xfa\x02\nentityName\xe0A\x02'
    _globals['_SEARCHENTITIESREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_SEARCHENTITIESREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x02'
    _globals['_SEARCHENTITIESREQUEST'].fields_by_name['terms']._loaded_options = None
    _globals['_SEARCHENTITIESREQUEST'].fields_by_name['terms']._serialized_options = b'\xe0A\x02'
    _globals['_ENTITYSERVICE'].methods_by_name['ListEntityTypes']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['ListEntityTypes']._serialized_options = b'\x92A\x13\x12\x11List entity types\x82\xd3\xe4\x93\x02\x11\x12\x0f/v1/entityTypes'
    _globals['_ENTITYSERVICE'].methods_by_name['GetEntityType']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['GetEntityType']._serialized_options = b'\x92A\x11\x12\x0fGet entity type\x82\xd3\xe4\x93\x02\x1a\x12\x18/v1/{name=entityTypes/*}'
    _globals['_ENTITYSERVICE'].methods_by_name['CreateEntityType']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['CreateEntityType']._serialized_options = b'\x92A\x14\x12\x12Create entity type\x82\xd3\xe4\x93\x02\x1e"\x0f/v1/entityTypes:\x0bentity_type'
    _globals['_ENTITYSERVICE'].methods_by_name['UpdateEntityType']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['UpdateEntityType']._serialized_options = b'\x92A\x14\x12\x12Update entity type\x82\xd3\xe4\x93\x0232$/v1/{entity_type.name=entityTypes/*}:\x0bentity_type'
    _globals['_ENTITYSERVICE'].methods_by_name['DeleteEntityType']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['DeleteEntityType']._serialized_options = b'\x92A\x14\x12\x12Delete entity type\x82\xd3\xe4\x93\x02\x1a*\x18/v1/{name=entityTypes/*}'
    _globals['_ENTITYSERVICE'].methods_by_name['ListEntities']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['ListEntities']._serialized_options = b'\x92A\x0f\x12\rList entities\x82\xd3\xe4\x93\x02%\x12#/v1/{parent=entityTypes/*}/entities'
    _globals['_ENTITYSERVICE'].methods_by_name['DeleteEntities']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['DeleteEntities']._serialized_options = b'\x92A\x18\x12\x16Delete entities (bulk)\x82\xd3\xe4\x93\x02%*#/v1/{parent=entityTypes/*}/entities'
    _globals['_ENTITYSERVICE'].methods_by_name['GetEntity']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['GetEntity']._serialized_options = b'\x92A\x0c\x12\nGet entity\x82\xd3\xe4\x93\x02%\x12#/v1/{name=entityTypes/*/entities/*}'
    _globals['_ENTITYSERVICE'].methods_by_name['CreateEntity']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['CreateEntity']._serialized_options = b'\x92A\x0f\x12\rCreate entity\x82\xd3\xe4\x93\x02-"#/v1/{parent=entityTypes/*}/entities:\x06entity'
    _globals['_ENTITYSERVICE'].methods_by_name['UpdateEntity']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['UpdateEntity']._serialized_options = b'\x92A\x0f\x12\rUpdate entity\x82\xd3\xe4\x93\x0242*/v1/{entity.name=entityTypes/*/entities/*}:\x06entity'
    _globals['_ENTITYSERVICE'].methods_by_name['DeleteEntity']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['DeleteEntity']._serialized_options = b'\x92A\x0f\x12\rDelete entity\x82\xd3\xe4\x93\x02%*#/v1/{name=entityTypes/*/entities/*}'
    _globals['_ENTITYSERVICE'].methods_by_name['SearchEntities']._loaded_options = None
    _globals['_ENTITYSERVICE'].methods_by_name['SearchEntities']._serialized_options = b'\x92A\x11\x12\x0fSearch entities\x82\xd3\xe4\x93\x02/"*/v1/{parent=entityTypes/*}/entities:search:\x01*'
    _globals['_LISTENTITYTYPESREQUEST']._serialized_start = 321
    _globals['_LISTENTITYTYPESREQUEST']._serialized_end = 384
    _globals['_LISTENTITYTYPESRESPONSE']._serialized_start = 386
    _globals['_LISTENTITYTYPESRESPONSE']._serialized_end = 510
    _globals['_GETENTITYTYPEREQUEST']._serialized_start = 512
    _globals['_GETENTITYTYPEREQUEST']._serialized_end = 576
    _globals['_CREATEENTITYTYPEREQUEST']._serialized_start = 578
    _globals['_CREATEENTITYTYPEREQUEST']._serialized_end = 684
    _globals['_UPDATEENTITYTYPEREQUEST']._serialized_start = 687
    _globals['_UPDATEENTITYTYPEREQUEST']._serialized_end = 865
    _globals['_DELETEENTITYTYPEREQUEST']._serialized_start = 867
    _globals['_DELETEENTITYTYPEREQUEST']._serialized_end = 934
    _globals['_LISTENTITIESREQUEST']._serialized_start = 936
    _globals['_LISTENTITIESREQUEST']._serialized_end = 1040
    _globals['_LISTENTITIESRESPONSE']._serialized_start = 1042
    _globals['_LISTENTITIESRESPONSE']._serialized_end = 1155
    _globals['_DELETEENTITIESREQUEST']._serialized_start = 1157
    _globals['_DELETEENTITIESREQUEST']._serialized_end = 1241
    _globals['_GETENTITYREQUEST']._serialized_start = 1243
    _globals['_GETENTITYREQUEST']._serialized_end = 1299
    _globals['_CREATEENTITYREQUEST']._serialized_start = 1301
    _globals['_CREATEENTITYREQUEST']._serialized_end = 1415
    _globals['_UPDATEENTITYREQUEST']._serialized_start = 1418
    _globals['_UPDATEENTITYREQUEST']._serialized_end = 1579
    _globals['_DELETEENTITYREQUEST']._serialized_start = 1581
    _globals['_DELETEENTITYREQUEST']._serialized_end = 1640
    _globals['_SEARCHENTITIESREQUEST']._serialized_start = 1643
    _globals['_SEARCHENTITIESREQUEST']._serialized_end = 1853
    _globals['_SEARCHENTITIESRESPONSE']._serialized_start = 1856
    _globals['_SEARCHENTITIESRESPONSE']._serialized_end = 2134
    _globals['_SEARCHENTITIESRESPONSE_SEARCHRESULT']._serialized_start = 2027
    _globals['_SEARCHENTITIESRESPONSE_SEARCHRESULT']._serialized_end = 2134
    _globals['_ENTITYSERVICE']._serialized_start = 2137
    _globals['_ENTITYSERVICE']._serialized_end = 4048