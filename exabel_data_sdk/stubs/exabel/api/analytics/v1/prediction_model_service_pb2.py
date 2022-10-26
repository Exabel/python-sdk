"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....exabel.api.analytics.v1 import prediction_model_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6exabel/api/analytics/v1/prediction_model_service.proto\x12\x17exabel.api.analytics.v1\x1a7exabel/api/analytics/v1/prediction_model_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x91\x01\n\x1fCreatePredictionModelRunRequest\x12/\n\x06parent\x18\x01 \x01(\tB\x1f\xe0A\x02\x92A\x19\xca>\x16\xfa\x02\x13predictionModelName\x12=\n\x03run\x18\x02 \x01(\x0b2+.exabel.api.analytics.v1.PredictionModelRunB\x03\xe0A\x022\xe8\x01\n\x16PredictionModelService\x12\xcd\x01\n\x18CreatePredictionModelRun\x128.exabel.api.analytics.v1.CreatePredictionModelRunRequest\x1a+.exabel.api.analytics.v1.PredictionModelRun"J\x82\xd3\xe4\x93\x02+"$/v1/{parent=predictionModels/*}/runs:\x03run\x92A\x16\x12\x14Run prediction modelBY\n\x1bcom.exabel.api.analytics.v1B\x1bPredictionModelServiceProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.prediction_model_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x1bPredictionModelServiceProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _CREATEPREDICTIONMODELRUNREQUEST.fields_by_name['parent']._options = None
    _CREATEPREDICTIONMODELRUNREQUEST.fields_by_name['parent']._serialized_options = b'\xe0A\x02\x92A\x19\xca>\x16\xfa\x02\x13predictionModelName'
    _CREATEPREDICTIONMODELRUNREQUEST.fields_by_name['run']._options = None
    _CREATEPREDICTIONMODELRUNREQUEST.fields_by_name['run']._serialized_options = b'\xe0A\x02'
    _PREDICTIONMODELSERVICE.methods_by_name['CreatePredictionModelRun']._options = None
    _PREDICTIONMODELSERVICE.methods_by_name['CreatePredictionModelRun']._serialized_options = b'\x82\xd3\xe4\x93\x02+"$/v1/{parent=predictionModels/*}/runs:\x03run\x92A\x16\x12\x14Run prediction model'
    _CREATEPREDICTIONMODELRUNREQUEST._serialized_start = 252
    _CREATEPREDICTIONMODELRUNREQUEST._serialized_end = 397
    _PREDICTIONMODELSERVICE._serialized_start = 400
    _PREDICTIONMODELSERVICE._serialized_end = 632