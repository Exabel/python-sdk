"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....exabel.api.data.v1 import data_set_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)exabel/api/data/v1/data_set_service.proto\x12\x12exabel.api.data.v1\x1a*exabel/api/data/v1/data_set_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x15\n\x13ListDataSetsRequest"F\n\x14ListDataSetsResponse\x12.\n\tdata_sets\x18\x01 \x03(\x0b2\x1b.exabel.api.data.v1.DataSet";\n\x11GetDataSetRequest\x12&\n\x04name\x18\x01 \x01(\tB\x18\x92A\x11\xca>\x0e\xfa\x02\x0bdataSetName\xe2A\x01\x02"K\n\x14CreateDataSetRequest\x123\n\x08data_set\x18\x01 \x01(\x0b2\x1b.exabel.api.data.v1.DataSetB\x04\xe2A\x01\x02"\x93\x01\n\x14UpdateDataSetRequest\x123\n\x08data_set\x18\x01 \x01(\x0b2\x1b.exabel.api.data.v1.DataSetB\x04\xe2A\x01\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask\x12\x15\n\rallow_missing\x18\x03 \x01(\x08">\n\x14DeleteDataSetRequest\x12&\n\x04name\x18\x01 \x01(\tB\x18\x92A\x11\xca>\x0e\xfa\x02\x0bdataSetName\xe2A\x01\x022\xd3\x05\n\x0eDataSetService\x12\x8a\x01\n\x0cListDataSets\x12\'.exabel.api.data.v1.ListDataSetsRequest\x1a(.exabel.api.data.v1.ListDataSetsResponse"\'\x92A\x10\x12\x0eList data sets\x82\xd3\xe4\x93\x02\x0e\x12\x0c/v1/dataSets\x12\x80\x01\n\nGetDataSet\x12%.exabel.api.data.v1.GetDataSetRequest\x1a\x1b.exabel.api.data.v1.DataSet".\x92A\x0e\x12\x0cGet data set\x82\xd3\xe4\x93\x02\x17\x12\x15/v1/{name=dataSets/*}\x12\x8a\x01\n\rCreateDataSet\x12(.exabel.api.data.v1.CreateDataSetRequest\x1a\x1b.exabel.api.data.v1.DataSet"2\x92A\x11\x12\x0fCreate data set\x82\xd3\xe4\x93\x02\x18"\x0c/v1/dataSets:\x08data_set\x12\x9c\x01\n\rUpdateDataSet\x12(.exabel.api.data.v1.UpdateDataSetRequest\x1a\x1b.exabel.api.data.v1.DataSet"D\x92A\x11\x12\x0fUpdate data set\x82\xd3\xe4\x93\x02*2\x1e/v1/{data_set.name=dataSets/*}:\x08data_set\x12\x84\x01\n\rDeleteDataSet\x12(.exabel.api.data.v1.DeleteDataSetRequest\x1a\x16.google.protobuf.Empty"1\x92A\x11\x12\x0fDelete data set\x82\xd3\xe4\x93\x02\x17*\x15/v1/{name=dataSets/*}BG\n\x16com.exabel.api.data.v1B\x13DataSetServiceProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.data_set_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals['DESCRIPTOR']._options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x13DataSetServiceProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_GETDATASETREQUEST'].fields_by_name['name']._options = None
    _globals['_GETDATASETREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x11\xca>\x0e\xfa\x02\x0bdataSetName\xe2A\x01\x02'
    _globals['_CREATEDATASETREQUEST'].fields_by_name['data_set']._options = None
    _globals['_CREATEDATASETREQUEST'].fields_by_name['data_set']._serialized_options = b'\xe2A\x01\x02'
    _globals['_UPDATEDATASETREQUEST'].fields_by_name['data_set']._options = None
    _globals['_UPDATEDATASETREQUEST'].fields_by_name['data_set']._serialized_options = b'\xe2A\x01\x02'
    _globals['_DELETEDATASETREQUEST'].fields_by_name['name']._options = None
    _globals['_DELETEDATASETREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x11\xca>\x0e\xfa\x02\x0bdataSetName\xe2A\x01\x02'
    _globals['_DATASETSERVICE'].methods_by_name['ListDataSets']._options = None
    _globals['_DATASETSERVICE'].methods_by_name['ListDataSets']._serialized_options = b'\x92A\x10\x12\x0eList data sets\x82\xd3\xe4\x93\x02\x0e\x12\x0c/v1/dataSets'
    _globals['_DATASETSERVICE'].methods_by_name['GetDataSet']._options = None
    _globals['_DATASETSERVICE'].methods_by_name['GetDataSet']._serialized_options = b'\x92A\x0e\x12\x0cGet data set\x82\xd3\xe4\x93\x02\x17\x12\x15/v1/{name=dataSets/*}'
    _globals['_DATASETSERVICE'].methods_by_name['CreateDataSet']._options = None
    _globals['_DATASETSERVICE'].methods_by_name['CreateDataSet']._serialized_options = b'\x92A\x11\x12\x0fCreate data set\x82\xd3\xe4\x93\x02\x18"\x0c/v1/dataSets:\x08data_set'
    _globals['_DATASETSERVICE'].methods_by_name['UpdateDataSet']._options = None
    _globals['_DATASETSERVICE'].methods_by_name['UpdateDataSet']._serialized_options = b'\x92A\x11\x12\x0fUpdate data set\x82\xd3\xe4\x93\x02*2\x1e/v1/{data_set.name=dataSets/*}:\x08data_set'
    _globals['_DATASETSERVICE'].methods_by_name['DeleteDataSet']._options = None
    _globals['_DATASETSERVICE'].methods_by_name['DeleteDataSet']._serialized_options = b'\x92A\x11\x12\x0fDelete data set\x82\xd3\xe4\x93\x02\x17*\x15/v1/{name=dataSets/*}'
    _globals['_LISTDATASETSREQUEST']._serialized_start = 283
    _globals['_LISTDATASETSREQUEST']._serialized_end = 304
    _globals['_LISTDATASETSRESPONSE']._serialized_start = 306
    _globals['_LISTDATASETSRESPONSE']._serialized_end = 376
    _globals['_GETDATASETREQUEST']._serialized_start = 378
    _globals['_GETDATASETREQUEST']._serialized_end = 437
    _globals['_CREATEDATASETREQUEST']._serialized_start = 439
    _globals['_CREATEDATASETREQUEST']._serialized_end = 514
    _globals['_UPDATEDATASETREQUEST']._serialized_start = 517
    _globals['_UPDATEDATASETREQUEST']._serialized_end = 664
    _globals['_DELETEDATASETREQUEST']._serialized_start = 666
    _globals['_DELETEDATASETREQUEST']._serialized_end = 728
    _globals['_DATASETSERVICE']._serialized_start = 731
    _globals['_DATASETSERVICE']._serialized_end = 1454