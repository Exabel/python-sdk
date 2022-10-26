"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7exabel/api/analytics/v1/prediction_model_messages.proto\x12\x17exabel.api.analytics.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"~\n\x12PredictionModelRun\x123\n\x04name\x18\x01 \x01(\tB%\xe0A\x03\x92A\x1fJ\x1d"predictionModels/123/runs/3"\x123\n\x0bdescription\x18\x02 \x01(\tB\x1e\x92A\x1bJ\x19"Initated by API request"BZ\n\x1bcom.exabel.api.analytics.v1B\x1cPredictionModelMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.prediction_model_messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x1cPredictionModelMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _PREDICTIONMODELRUN.fields_by_name['name']._options = None
    _PREDICTIONMODELRUN.fields_by_name['name']._serialized_options = b'\xe0A\x03\x92A\x1fJ\x1d"predictionModels/123/runs/3"'
    _PREDICTIONMODELRUN.fields_by_name['description']._options = None
    _PREDICTIONMODELRUN.fields_by_name['description']._serialized_options = b'\x92A\x1bJ\x19"Initated by API request"'
    _PREDICTIONMODELRUN._serialized_start = 165
    _PREDICTIONMODELRUN._serialized_end = 291