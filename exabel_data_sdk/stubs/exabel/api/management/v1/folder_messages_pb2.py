"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/management/v1/folder_messages.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.management.v1 import user_messages_pb2 as exabel_dot_api_dot_management_dot_v1_dot_user__messages__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.exabel/api/management/v1/folder_messages.proto\x12\x18exabel.api.management.v1\x1a,exabel/api/management/v1/user_messages.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xf3\x01\n\x06Folder\x120\n\x04name\x18\x01 \x01(\tB"\x92A\x1fJ\r"folders/123"\xca>\r\xfa\x02\nfolderName\x120\n\x0cdisplay_name\x18\x02 \x01(\tB\x1a\x92A\x14J\x12"My shared folder"\xe0A\x02\x124\n\x0bdescription\x18\x05 \x01(\tB\x1f\x92A\x1cJ\x1a"This is my shared folder"\x12\x12\n\x05write\x18\x03 \x01(\x08B\x03\xe0A\x03\x12;\n\x05items\x18\x04 \x03(\x0b2$.exabel.api.management.v1.FolderItemB\x06\xe0A\x06\xe0A\x03"\xf0\x02\n\nFolderItem\x122\n\x06parent\x18\x01 \x01(\tB"\x92A\x1fJ\r"folders/123"\xca>\r\xfa\x02\nfolderName\x12*\n\x04name\x18\x02 \x01(\tB\x1c\x92A\x16J\x14"derivedSignals/123"\xe0A\x03\x12&\n\x0cdisplay_name\x18\x03 \x01(\tB\x10\x92A\rJ\x0b"my_signal"\x12\x13\n\x0bdescription\x18\t \x01(\t\x12;\n\titem_type\x18\x04 \x01(\x0e2(.exabel.api.management.v1.FolderItemType\x12/\n\x0bcreate_time\x18\x05 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12/\n\x0bupdate_time\x18\x06 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x12\n\ncreated_by\x18\x07 \x01(\t\x12\x12\n\nupdated_by\x18\x08 \x01(\t"O\n\x0eFolderAccessor\x12.\n\x05group\x18\x01 \x01(\x0b2\x1f.exabel.api.management.v1.Group\x12\r\n\x05write\x18\x02 \x01(\x08"B\n\x0cSearchResult\x122\n\x04item\x18\x01 \x01(\x0b2$.exabel.api.management.v1.FolderItem*\xe0\x01\n\x0eFolderItemType\x12\x1c\n\x18FOLDER_ITEM_TYPE_INVALID\x10\x00\x12\x12\n\x0eDERIVED_SIGNAL\x10\x01\x12\x14\n\x10PREDICTION_MODEL\x10\x02\x12\x16\n\x12PORTFOLIO_STRATEGY\x10\x03\x12\r\n\tDASHBOARD\x10\x04\x12\x0e\n\nDRILL_DOWN\x10\x05\x12\x07\n\x03TAG\x10\x06\x12\n\n\x06SCREEN\x10\x07\x12\x13\n\x0fFINANCIAL_MODEL\x10\x08\x12\t\n\x05CHART\x10\t\x12\x0f\n\x0bKPI_MAPPING\x10\n\x12\t\n\x05ALERT\x10\x0bBS\n\x1ccom.exabel.api.management.v1B\x13FolderMessagesProtoP\x01Z\x1cexabel.com/api/management/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.management.v1.folder_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1ccom.exabel.api.management.v1B\x13FolderMessagesProtoP\x01Z\x1cexabel.com/api/management/v1'
    _globals['_FOLDER'].fields_by_name['name']._loaded_options = None
    _globals['_FOLDER'].fields_by_name['name']._serialized_options = b'\x92A\x1fJ\r"folders/123"\xca>\r\xfa\x02\nfolderName'
    _globals['_FOLDER'].fields_by_name['display_name']._loaded_options = None
    _globals['_FOLDER'].fields_by_name['display_name']._serialized_options = b'\x92A\x14J\x12"My shared folder"\xe0A\x02'
    _globals['_FOLDER'].fields_by_name['description']._loaded_options = None
    _globals['_FOLDER'].fields_by_name['description']._serialized_options = b'\x92A\x1cJ\x1a"This is my shared folder"'
    _globals['_FOLDER'].fields_by_name['write']._loaded_options = None
    _globals['_FOLDER'].fields_by_name['write']._serialized_options = b'\xe0A\x03'
    _globals['_FOLDER'].fields_by_name['items']._loaded_options = None
    _globals['_FOLDER'].fields_by_name['items']._serialized_options = b'\xe0A\x06\xe0A\x03'
    _globals['_FOLDERITEM'].fields_by_name['parent']._loaded_options = None
    _globals['_FOLDERITEM'].fields_by_name['parent']._serialized_options = b'\x92A\x1fJ\r"folders/123"\xca>\r\xfa\x02\nfolderName'
    _globals['_FOLDERITEM'].fields_by_name['name']._loaded_options = None
    _globals['_FOLDERITEM'].fields_by_name['name']._serialized_options = b'\x92A\x16J\x14"derivedSignals/123"\xe0A\x03'
    _globals['_FOLDERITEM'].fields_by_name['display_name']._loaded_options = None
    _globals['_FOLDERITEM'].fields_by_name['display_name']._serialized_options = b'\x92A\rJ\x0b"my_signal"'
    _globals['_FOLDERITEMTYPE']._serialized_start = 1003
    _globals['_FOLDERITEMTYPE']._serialized_end = 1227
    _globals['_FOLDER']._serialized_start = 237
    _globals['_FOLDER']._serialized_end = 480
    _globals['_FOLDERITEM']._serialized_start = 483
    _globals['_FOLDERITEM']._serialized_end = 851
    _globals['_FOLDERACCESSOR']._serialized_start = 853
    _globals['_FOLDERACCESSOR']._serialized_end = 932
    _globals['_SEARCHRESULT']._serialized_start = 934
    _globals['_SEARCHRESULT']._serialized_end = 1000