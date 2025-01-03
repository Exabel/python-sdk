"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/analytics/v1/prediction_model_messages.proto')
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7exabel/api/analytics/v1/prediction_model_messages.proto\x12\x17exabel.api.analytics.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x96\x02\n\x12PredictionModelRun\x123\n\x04name\x18\x01 \x01(\tB%\x92A\x1fJ\x1d"predictionModels/123/runs/3"\xe0A\x03\x124\n\x0bdescription\x18\x02 \x01(\tB\x1f\x92A\x1cJ\x1a"Initiated by API request"\x12B\n\rconfiguration\x18\x03 \x01(\x0e2+.exabel.api.analytics.v1.ModelConfiguration\x12!\n\x14configuration_source\x18\x04 \x01(\x05H\x00\x88\x01\x01\x12\x15\n\rauto_activate\x18\x05 \x01(\x08B\x17\n\x15_configuration_source*e\n\x12ModelConfiguration\x12%\n!MODEL_CONFIGURATION_NOT_SPECIFIED\x10\x00\x12\n\n\x06LATEST\x10\x01\x12\n\n\x06ACTIVE\x10\x02\x12\x10\n\x0cSPECIFIC_RUN\x10\x03BZ\n\x1bcom.exabel.api.analytics.v1B\x1cPredictionModelMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.prediction_model_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x1cPredictionModelMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _globals['_PREDICTIONMODELRUN'].fields_by_name['name']._loaded_options = None
    _globals['_PREDICTIONMODELRUN'].fields_by_name['name']._serialized_options = b'\x92A\x1fJ\x1d"predictionModels/123/runs/3"\xe0A\x03'
    _globals['_PREDICTIONMODELRUN'].fields_by_name['description']._loaded_options = None
    _globals['_PREDICTIONMODELRUN'].fields_by_name['description']._serialized_options = b'\x92A\x1cJ\x1a"Initiated by API request"'
    _globals['_MODELCONFIGURATION']._serialized_start = 446
    _globals['_MODELCONFIGURATION']._serialized_end = 547
    _globals['_PREDICTIONMODELRUN']._serialized_start = 166
    _globals['_PREDICTIONMODELRUN']._serialized_end = 444