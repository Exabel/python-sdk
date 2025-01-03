"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/management/v1/library_service.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.management.v1 import folder_messages_pb2 as exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.exabel/api/management/v1/library_service.proto\x12\x18exabel.api.management.v1\x1a.exabel/api/management/v1/folder_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x14\n\x12ListFoldersRequest"H\n\x13ListFoldersResponse\x121\n\x07folders\x18\x01 \x03(\x0b2 .exabel.api.management.v1.Folder"8\n\x10GetFolderRequest\x12$\n\x04name\x18\x01 \x01(\tB\x16\x92A\x10\xca>\r\xfa\x02\nfolderName\xe0A\x02"L\n\x13CreateFolderRequest\x125\n\x06folder\x18\x01 \x01(\x0b2 .exabel.api.management.v1.FolderB\x03\xe0A\x02"\x94\x01\n\x13UpdateFolderRequest\x125\n\x06folder\x18\x01 \x01(\x0b2 .exabel.api.management.v1.FolderB\x03\xe0A\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask\x12\x15\n\rallow_missing\x18\x03 \x01(\x08";\n\x13DeleteFolderRequest\x12$\n\x04name\x18\x01 \x01(\tB\x16\x92A\x10\xca>\r\xfa\x02\nfolderName\xe0A\x02"\x86\x01\n\x10ListItemsRequest\x125\n\x06parent\x18\x01 \x01(\tB%\x92A\x1fJ\r"folders/123"\xca>\r\xfa\x02\nfolderName\xe0A\x01\x12;\n\titem_type\x18\x02 \x01(\x0e2(.exabel.api.management.v1.FolderItemType"H\n\x11ListItemsResponse\x123\n\x05items\x18\x01 \x03(\x0b2$.exabel.api.management.v1.FolderItem"U\n\x10MoveItemsRequest\x12\x12\n\x05items\x18\x01 \x03(\tB\x03\xe0A\x02\x12-\n\rtarget_folder\x18\x02 \x01(\tB\x16\x92A\x10\xca>\r\xfa\x02\nfolderName\xe0A\x02"\x13\n\x11MoveItemsResponse"?\n\x1aListFolderAccessorsRequest\x12!\n\x04name\x18\x01 \x01(\tB\x13\x92A\x10\xca>\r\xfa\x02\nfolderName"a\n\x1bListFolderAccessorsResponse\x12B\n\x10folder_accessors\x18\x01 \x03(\x0b2(.exabel.api.management.v1.FolderAccessor"y\n\x12ShareFolderRequest\x122\n\x06folder\x18\x01 \x01(\tB"\x92A\x1fJ\r"folders/123"\xca>\r\xfa\x02\nfolderName\x12 \n\x05group\x18\x02 \x01(\tB\x11\x92A\x0eJ\x0c"groups/123"\x12\r\n\x05write\x18\x03 \x01(\x08"l\n\x14UnshareFolderRequest\x122\n\x06folder\x18\x01 \x01(\tB"\x92A\x1fJ\r"folders/123"\xca>\r\xfa\x02\nfolderName\x12 \n\x05group\x18\x02 \x01(\tB\x11\x92A\x0eJ\x0c"groups/123""\xd0\x01\n\x12SearchItemsRequest\x12=\n\x06folder\x18\x01 \x01(\tB-\x92A\'J\x0b"folders/-"\xca>\x17\xfa\x02\x14folderNameAllFolders\xe0A\x02\x12\x12\n\x05query\x18\x02 \x01(\tB\x03\xe0A\x02\x12@\n\titem_type\x18\x03 \x01(\x0e2(.exabel.api.management.v1.FolderItemTypeB\x03\xe0A\x01\x12\x12\n\npage_token\x18\x04 \x01(\t\x12\x11\n\tpage_size\x18\x05 \x01(\x05"g\n\x13SearchItemsResponse\x127\n\x07results\x18\x01 \x03(\x0b2&.exabel.api.management.v1.SearchResult\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t2\xdc\r\n\x0eLibraryService\x12\x90\x01\n\x0bListFolders\x12,.exabel.api.management.v1.ListFoldersRequest\x1a-.exabel.api.management.v1.ListFoldersResponse"$\x92A\x0e\x12\x0cList folders\x82\xd3\xe4\x93\x02\r\x12\x0b/v1/folders\x12\x86\x01\n\tGetFolder\x12*.exabel.api.management.v1.GetFolderRequest\x1a .exabel.api.management.v1.Folder"+\x92A\x0c\x12\nGet folder\x82\xd3\xe4\x93\x02\x16\x12\x14/v1/{name=folders/*}\x12\x8e\x01\n\x0cCreateFolder\x12-.exabel.api.management.v1.CreateFolderRequest\x1a .exabel.api.management.v1.Folder"-\x92A\x0f\x12\rCreate folder\x82\xd3\xe4\x93\x02\x15"\x0b/v1/folders:\x06folder\x12\x9e\x01\n\x0cUpdateFolder\x12-.exabel.api.management.v1.UpdateFolderRequest\x1a .exabel.api.management.v1.Folder"=\x92A\x0f\x12\rUpdate folder\x82\xd3\xe4\x93\x02%2\x1b/v1/{folder.name=folders/*}:\x06folder\x12\x85\x01\n\x0cDeleteFolder\x12-.exabel.api.management.v1.DeleteFolderRequest\x1a\x16.google.protobuf.Empty".\x92A\x0f\x12\rDelete folder\x82\xd3\xe4\x93\x02\x16*\x14/v1/{name=folders/*}\x12\xa0\x01\n\tListItems\x12*.exabel.api.management.v1.ListItemsRequest\x1a+.exabel.api.management.v1.ListItemsResponse":\x92A\x13\x12\x11List folder items\x82\xd3\xe4\x93\x02\x1e\x12\x1c/v1/{parent=folders/*}/items\x12\xab\x01\n\tMoveItems\x12*.exabel.api.management.v1.MoveItemsRequest\x1a+.exabel.api.management.v1.MoveItemsResponse"E\x92A\x13\x12\x11Move folder items\x82\xd3\xe4\x93\x02)"\'/v1/{target_folder=folders/*}:moveItems\x12\xc4\x01\n\x13ListFolderAccessors\x124.exabel.api.management.v1.ListFolderAccessorsRequest\x1a5.exabel.api.management.v1.ListFolderAccessorsResponse"@\x92A\x17\x12\x15List folder accessors\x82\xd3\xe4\x93\x02 \x12\x1e/v1/{name=folders/*}/accessors\x12\x8d\x01\n\x0bShareFolder\x12,.exabel.api.management.v1.ShareFolderRequest\x1a\x16.google.protobuf.Empty"8\x92A\x0e\x12\x0cShare folder\x82\xd3\xe4\x93\x02!"\x1c/v1/{folder=folders/*}:share:\x01*\x12\x95\x01\n\rUnshareFolder\x12..exabel.api.management.v1.UnshareFolderRequest\x1a\x16.google.protobuf.Empty"<\x92A\x10\x12\x0eUnshare folder\x82\xd3\xe4\x93\x02#"\x1e/v1/{folder=folders/*}:unshare:\x01*\x12\xb3\x01\n\x0bSearchItems\x12,.exabel.api.management.v1.SearchItemsRequest\x1a-.exabel.api.management.v1.SearchItemsResponse"G\x92A\x19\x12\x17Search for folder items\x82\xd3\xe4\x93\x02%\x12#/v1/{folder=folders/*}/items:searchBS\n\x1ccom.exabel.api.management.v1B\x13LibraryServiceProtoP\x01Z\x1cexabel.com/api/management/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.management.v1.library_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1ccom.exabel.api.management.v1B\x13LibraryServiceProtoP\x01Z\x1cexabel.com/api/management/v1'
    _globals['_GETFOLDERREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_GETFOLDERREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x10\xca>\r\xfa\x02\nfolderName\xe0A\x02'
    _globals['_CREATEFOLDERREQUEST'].fields_by_name['folder']._loaded_options = None
    _globals['_CREATEFOLDERREQUEST'].fields_by_name['folder']._serialized_options = b'\xe0A\x02'
    _globals['_UPDATEFOLDERREQUEST'].fields_by_name['folder']._loaded_options = None
    _globals['_UPDATEFOLDERREQUEST'].fields_by_name['folder']._serialized_options = b'\xe0A\x02'
    _globals['_DELETEFOLDERREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_DELETEFOLDERREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x10\xca>\r\xfa\x02\nfolderName\xe0A\x02'
    _globals['_LISTITEMSREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_LISTITEMSREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x1fJ\r"folders/123"\xca>\r\xfa\x02\nfolderName\xe0A\x01'
    _globals['_MOVEITEMSREQUEST'].fields_by_name['items']._loaded_options = None
    _globals['_MOVEITEMSREQUEST'].fields_by_name['items']._serialized_options = b'\xe0A\x02'
    _globals['_MOVEITEMSREQUEST'].fields_by_name['target_folder']._loaded_options = None
    _globals['_MOVEITEMSREQUEST'].fields_by_name['target_folder']._serialized_options = b'\x92A\x10\xca>\r\xfa\x02\nfolderName\xe0A\x02'
    _globals['_LISTFOLDERACCESSORSREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_LISTFOLDERACCESSORSREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x10\xca>\r\xfa\x02\nfolderName'
    _globals['_SHAREFOLDERREQUEST'].fields_by_name['folder']._loaded_options = None
    _globals['_SHAREFOLDERREQUEST'].fields_by_name['folder']._serialized_options = b'\x92A\x1fJ\r"folders/123"\xca>\r\xfa\x02\nfolderName'
    _globals['_SHAREFOLDERREQUEST'].fields_by_name['group']._loaded_options = None
    _globals['_SHAREFOLDERREQUEST'].fields_by_name['group']._serialized_options = b'\x92A\x0eJ\x0c"groups/123"'
    _globals['_UNSHAREFOLDERREQUEST'].fields_by_name['folder']._loaded_options = None
    _globals['_UNSHAREFOLDERREQUEST'].fields_by_name['folder']._serialized_options = b'\x92A\x1fJ\r"folders/123"\xca>\r\xfa\x02\nfolderName'
    _globals['_UNSHAREFOLDERREQUEST'].fields_by_name['group']._loaded_options = None
    _globals['_UNSHAREFOLDERREQUEST'].fields_by_name['group']._serialized_options = b'\x92A\x0eJ\x0c"groups/123"'
    _globals['_SEARCHITEMSREQUEST'].fields_by_name['folder']._loaded_options = None
    _globals['_SEARCHITEMSREQUEST'].fields_by_name['folder']._serialized_options = b'\x92A\'J\x0b"folders/-"\xca>\x17\xfa\x02\x14folderNameAllFolders\xe0A\x02'
    _globals['_SEARCHITEMSREQUEST'].fields_by_name['query']._loaded_options = None
    _globals['_SEARCHITEMSREQUEST'].fields_by_name['query']._serialized_options = b'\xe0A\x02'
    _globals['_SEARCHITEMSREQUEST'].fields_by_name['item_type']._loaded_options = None
    _globals['_SEARCHITEMSREQUEST'].fields_by_name['item_type']._serialized_options = b'\xe0A\x01'
    _globals['_LIBRARYSERVICE'].methods_by_name['ListFolders']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['ListFolders']._serialized_options = b'\x92A\x0e\x12\x0cList folders\x82\xd3\xe4\x93\x02\r\x12\x0b/v1/folders'
    _globals['_LIBRARYSERVICE'].methods_by_name['GetFolder']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['GetFolder']._serialized_options = b'\x92A\x0c\x12\nGet folder\x82\xd3\xe4\x93\x02\x16\x12\x14/v1/{name=folders/*}'
    _globals['_LIBRARYSERVICE'].methods_by_name['CreateFolder']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['CreateFolder']._serialized_options = b'\x92A\x0f\x12\rCreate folder\x82\xd3\xe4\x93\x02\x15"\x0b/v1/folders:\x06folder'
    _globals['_LIBRARYSERVICE'].methods_by_name['UpdateFolder']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['UpdateFolder']._serialized_options = b'\x92A\x0f\x12\rUpdate folder\x82\xd3\xe4\x93\x02%2\x1b/v1/{folder.name=folders/*}:\x06folder'
    _globals['_LIBRARYSERVICE'].methods_by_name['DeleteFolder']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['DeleteFolder']._serialized_options = b'\x92A\x0f\x12\rDelete folder\x82\xd3\xe4\x93\x02\x16*\x14/v1/{name=folders/*}'
    _globals['_LIBRARYSERVICE'].methods_by_name['ListItems']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['ListItems']._serialized_options = b'\x92A\x13\x12\x11List folder items\x82\xd3\xe4\x93\x02\x1e\x12\x1c/v1/{parent=folders/*}/items'
    _globals['_LIBRARYSERVICE'].methods_by_name['MoveItems']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['MoveItems']._serialized_options = b'\x92A\x13\x12\x11Move folder items\x82\xd3\xe4\x93\x02)"\'/v1/{target_folder=folders/*}:moveItems'
    _globals['_LIBRARYSERVICE'].methods_by_name['ListFolderAccessors']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['ListFolderAccessors']._serialized_options = b'\x92A\x17\x12\x15List folder accessors\x82\xd3\xe4\x93\x02 \x12\x1e/v1/{name=folders/*}/accessors'
    _globals['_LIBRARYSERVICE'].methods_by_name['ShareFolder']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['ShareFolder']._serialized_options = b'\x92A\x0e\x12\x0cShare folder\x82\xd3\xe4\x93\x02!"\x1c/v1/{folder=folders/*}:share:\x01*'
    _globals['_LIBRARYSERVICE'].methods_by_name['UnshareFolder']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['UnshareFolder']._serialized_options = b'\x92A\x10\x12\x0eUnshare folder\x82\xd3\xe4\x93\x02#"\x1e/v1/{folder=folders/*}:unshare:\x01*'
    _globals['_LIBRARYSERVICE'].methods_by_name['SearchItems']._loaded_options = None
    _globals['_LIBRARYSERVICE'].methods_by_name['SearchItems']._serialized_options = b'\x92A\x19\x12\x17Search for folder items\x82\xd3\xe4\x93\x02%\x12#/v1/{folder=folders/*}/items:search'
    _globals['_LISTFOLDERSREQUEST']._serialized_start = 298
    _globals['_LISTFOLDERSREQUEST']._serialized_end = 318
    _globals['_LISTFOLDERSRESPONSE']._serialized_start = 320
    _globals['_LISTFOLDERSRESPONSE']._serialized_end = 392
    _globals['_GETFOLDERREQUEST']._serialized_start = 394
    _globals['_GETFOLDERREQUEST']._serialized_end = 450
    _globals['_CREATEFOLDERREQUEST']._serialized_start = 452
    _globals['_CREATEFOLDERREQUEST']._serialized_end = 528
    _globals['_UPDATEFOLDERREQUEST']._serialized_start = 531
    _globals['_UPDATEFOLDERREQUEST']._serialized_end = 679
    _globals['_DELETEFOLDERREQUEST']._serialized_start = 681
    _globals['_DELETEFOLDERREQUEST']._serialized_end = 740
    _globals['_LISTITEMSREQUEST']._serialized_start = 743
    _globals['_LISTITEMSREQUEST']._serialized_end = 877
    _globals['_LISTITEMSRESPONSE']._serialized_start = 879
    _globals['_LISTITEMSRESPONSE']._serialized_end = 951
    _globals['_MOVEITEMSREQUEST']._serialized_start = 953
    _globals['_MOVEITEMSREQUEST']._serialized_end = 1038
    _globals['_MOVEITEMSRESPONSE']._serialized_start = 1040
    _globals['_MOVEITEMSRESPONSE']._serialized_end = 1059
    _globals['_LISTFOLDERACCESSORSREQUEST']._serialized_start = 1061
    _globals['_LISTFOLDERACCESSORSREQUEST']._serialized_end = 1124
    _globals['_LISTFOLDERACCESSORSRESPONSE']._serialized_start = 1126
    _globals['_LISTFOLDERACCESSORSRESPONSE']._serialized_end = 1223
    _globals['_SHAREFOLDERREQUEST']._serialized_start = 1225
    _globals['_SHAREFOLDERREQUEST']._serialized_end = 1346
    _globals['_UNSHAREFOLDERREQUEST']._serialized_start = 1348
    _globals['_UNSHAREFOLDERREQUEST']._serialized_end = 1456
    _globals['_SEARCHITEMSREQUEST']._serialized_start = 1459
    _globals['_SEARCHITEMSREQUEST']._serialized_end = 1667
    _globals['_SEARCHITEMSRESPONSE']._serialized_start = 1669
    _globals['_SEARCHITEMSRESPONSE']._serialized_end = 1772
    _globals['_LIBRARYSERVICE']._serialized_start = 1775
    _globals['_LIBRARYSERVICE']._serialized_end = 3531