"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'protoc_gen_openapiv2/options/openapiv2.proto')
_sym_db = _symbol_database.Default()
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,protoc_gen_openapiv2/options/openapiv2.proto\x12)grpc.gateway.protoc_gen_openapiv2.options\x1a\x1cgoogle/protobuf/struct.proto"\xdd\x06\n\x07Swagger\x12\x0f\n\x07swagger\x18\x01 \x01(\t\x12=\n\x04info\x18\x02 \x01(\x0b2/.grpc.gateway.protoc_gen_openapiv2.options.Info\x12\x0c\n\x04host\x18\x03 \x01(\t\x12\x11\n\tbase_path\x18\x04 \x01(\t\x12B\n\x07schemes\x18\x05 \x03(\x0e21.grpc.gateway.protoc_gen_openapiv2.options.Scheme\x12\x10\n\x08consumes\x18\x06 \x03(\t\x12\x10\n\x08produces\x18\x07 \x03(\t\x12T\n\tresponses\x18\n \x03(\x0b2A.grpc.gateway.protoc_gen_openapiv2.options.Swagger.ResponsesEntry\x12\\\n\x14security_definitions\x18\x0b \x01(\x0b2>.grpc.gateway.protoc_gen_openapiv2.options.SecurityDefinitions\x12P\n\x08security\x18\x0c \x03(\x0b2>.grpc.gateway.protoc_gen_openapiv2.options.SecurityRequirement\x12W\n\rexternal_docs\x18\x0e \x01(\x0b2@.grpc.gateway.protoc_gen_openapiv2.options.ExternalDocumentation\x12V\n\nextensions\x18\x0f \x03(\x0b2B.grpc.gateway.protoc_gen_openapiv2.options.Swagger.ExtensionsEntry\x1ae\n\x0eResponsesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12B\n\x05value\x18\x02 \x01(\x0b23.grpc.gateway.protoc_gen_openapiv2.options.Response:\x028\x01\x1aI\n\x0fExtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b2\x16.google.protobuf.Value:\x028\x01J\x04\x08\x08\x10\tJ\x04\x08\t\x10\nJ\x04\x08\r\x10\x0e"\xe6\x05\n\tOperation\x12\x0c\n\x04tags\x18\x01 \x03(\t\x12\x0f\n\x07summary\x18\x02 \x01(\t\x12\x13\n\x0bdescription\x18\x03 \x01(\t\x12W\n\rexternal_docs\x18\x04 \x01(\x0b2@.grpc.gateway.protoc_gen_openapiv2.options.ExternalDocumentation\x12\x14\n\x0coperation_id\x18\x05 \x01(\t\x12\x10\n\x08consumes\x18\x06 \x03(\t\x12\x10\n\x08produces\x18\x07 \x03(\t\x12V\n\tresponses\x18\t \x03(\x0b2C.grpc.gateway.protoc_gen_openapiv2.options.Operation.ResponsesEntry\x12B\n\x07schemes\x18\n \x03(\x0e21.grpc.gateway.protoc_gen_openapiv2.options.Scheme\x12\x12\n\ndeprecated\x18\x0b \x01(\x08\x12P\n\x08security\x18\x0c \x03(\x0b2>.grpc.gateway.protoc_gen_openapiv2.options.SecurityRequirement\x12X\n\nextensions\x18\r \x03(\x0b2D.grpc.gateway.protoc_gen_openapiv2.options.Operation.ExtensionsEntry\x1ae\n\x0eResponsesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12B\n\x05value\x18\x02 \x01(\x0b23.grpc.gateway.protoc_gen_openapiv2.options.Response:\x028\x01\x1aI\n\x0fExtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b2\x16.google.protobuf.Value:\x028\x01J\x04\x08\x08\x10\t"\xab\x01\n\x06Header\x12\x13\n\x0bdescription\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0e\n\x06format\x18\x03 \x01(\t\x12\x0f\n\x07default\x18\x06 \x01(\t\x12\x0f\n\x07pattern\x18\r \x01(\tJ\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06J\x04\x08\x07\x10\x08J\x04\x08\x08\x10\tJ\x04\x08\t\x10\nJ\x04\x08\n\x10\x0bJ\x04\x08\x0b\x10\x0cJ\x04\x08\x0c\x10\rJ\x04\x08\x0e\x10\x0fJ\x04\x08\x0f\x10\x10J\x04\x08\x10\x10\x11J\x04\x08\x11\x10\x12J\x04\x08\x12\x10\x13"\xc2\x04\n\x08Response\x12\x13\n\x0bdescription\x18\x01 \x01(\t\x12A\n\x06schema\x18\x02 \x01(\x0b21.grpc.gateway.protoc_gen_openapiv2.options.Schema\x12Q\n\x07headers\x18\x03 \x03(\x0b2@.grpc.gateway.protoc_gen_openapiv2.options.Response.HeadersEntry\x12S\n\x08examples\x18\x04 \x03(\x0b2A.grpc.gateway.protoc_gen_openapiv2.options.Response.ExamplesEntry\x12W\n\nextensions\x18\x05 \x03(\x0b2C.grpc.gateway.protoc_gen_openapiv2.options.Response.ExtensionsEntry\x1aa\n\x0cHeadersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12@\n\x05value\x18\x02 \x01(\x0b21.grpc.gateway.protoc_gen_openapiv2.options.Header:\x028\x01\x1a/\n\rExamplesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01\x1aI\n\x0fExtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b2\x16.google.protobuf.Value:\x028\x01"\xff\x02\n\x04Info\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12\x18\n\x10terms_of_service\x18\x03 \x01(\t\x12C\n\x07contact\x18\x04 \x01(\x0b22.grpc.gateway.protoc_gen_openapiv2.options.Contact\x12C\n\x07license\x18\x05 \x01(\x0b22.grpc.gateway.protoc_gen_openapiv2.options.License\x12\x0f\n\x07version\x18\x06 \x01(\t\x12S\n\nextensions\x18\x07 \x03(\x0b2?.grpc.gateway.protoc_gen_openapiv2.options.Info.ExtensionsEntry\x1aI\n\x0fExtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b2\x16.google.protobuf.Value:\x028\x01"3\n\x07Contact\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\r\n\x05email\x18\x03 \x01(\t"$\n\x07License\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t"9\n\x15ExternalDocumentation\x12\x13\n\x0bdescription\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t"\xee\x01\n\x06Schema\x12J\n\x0bjson_schema\x18\x01 \x01(\x0b25.grpc.gateway.protoc_gen_openapiv2.options.JSONSchema\x12\x15\n\rdiscriminator\x18\x02 \x01(\t\x12\x11\n\tread_only\x18\x03 \x01(\x08\x12W\n\rexternal_docs\x18\x05 \x01(\x0b2@.grpc.gateway.protoc_gen_openapiv2.options.ExternalDocumentation\x12\x0f\n\x07example\x18\x06 \x01(\tJ\x04\x08\x04\x10\x05"\xfc\x06\n\nJSONSchema\x12\x0b\n\x03ref\x18\x03 \x01(\t\x12\r\n\x05title\x18\x05 \x01(\t\x12\x13\n\x0bdescription\x18\x06 \x01(\t\x12\x0f\n\x07default\x18\x07 \x01(\t\x12\x11\n\tread_only\x18\x08 \x01(\x08\x12\x0f\n\x07example\x18\t \x01(\t\x12\x13\n\x0bmultiple_of\x18\n \x01(\x01\x12\x0f\n\x07maximum\x18\x0b \x01(\x01\x12\x19\n\x11exclusive_maximum\x18\x0c \x01(\x08\x12\x0f\n\x07minimum\x18\r \x01(\x01\x12\x19\n\x11exclusive_minimum\x18\x0e \x01(\x08\x12\x12\n\nmax_length\x18\x0f \x01(\x04\x12\x12\n\nmin_length\x18\x10 \x01(\x04\x12\x0f\n\x07pattern\x18\x11 \x01(\t\x12\x11\n\tmax_items\x18\x14 \x01(\x04\x12\x11\n\tmin_items\x18\x15 \x01(\x04\x12\x14\n\x0cunique_items\x18\x16 \x01(\x08\x12\x16\n\x0emax_properties\x18\x18 \x01(\x04\x12\x16\n\x0emin_properties\x18\x19 \x01(\x04\x12\x10\n\x08required\x18\x1a \x03(\t\x12\r\n\x05array\x18" \x03(\t\x12Y\n\x04type\x18# \x03(\x0e2K.grpc.gateway.protoc_gen_openapiv2.options.JSONSchema.JSONSchemaSimpleTypes\x12\x0e\n\x06format\x18$ \x01(\t\x12\x0c\n\x04enum\x18. \x03(\t\x12f\n\x13field_configuration\x18\xe9\x07 \x01(\x0b2H.grpc.gateway.protoc_gen_openapiv2.options.JSONSchema.FieldConfiguration\x1a-\n\x12FieldConfiguration\x12\x17\n\x0fpath_param_name\x18/ \x01(\t"w\n\x15JSONSchemaSimpleTypes\x12\x0b\n\x07UNKNOWN\x10\x00\x12\t\n\x05ARRAY\x10\x01\x12\x0b\n\x07BOOLEAN\x10\x02\x12\x0b\n\x07INTEGER\x10\x03\x12\x08\n\x04NULL\x10\x04\x12\n\n\x06NUMBER\x10\x05\x12\n\n\x06OBJECT\x10\x06\x12\n\n\x06STRING\x10\x07J\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03J\x04\x08\x04\x10\x05J\x04\x08\x12\x10\x13J\x04\x08\x13\x10\x14J\x04\x08\x17\x10\x18J\x04\x08\x1b\x10\x1cJ\x04\x08\x1c\x10\x1dJ\x04\x08\x1d\x10\x1eJ\x04\x08\x1e\x10"J\x04\x08%\x10*J\x04\x08*\x10+J\x04\x08+\x10."y\n\x03Tag\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12W\n\rexternal_docs\x18\x03 \x01(\x0b2@.grpc.gateway.protoc_gen_openapiv2.options.ExternalDocumentationJ\x04\x08\x01\x10\x02"\xe1\x01\n\x13SecurityDefinitions\x12^\n\x08security\x18\x01 \x03(\x0b2L.grpc.gateway.protoc_gen_openapiv2.options.SecurityDefinitions.SecurityEntry\x1aj\n\rSecurityEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12H\n\x05value\x18\x02 \x01(\x0b29.grpc.gateway.protoc_gen_openapiv2.options.SecurityScheme:\x028\x01"\xa0\x06\n\x0eSecurityScheme\x12L\n\x04type\x18\x01 \x01(\x0e2>.grpc.gateway.protoc_gen_openapiv2.options.SecurityScheme.Type\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12H\n\x02in\x18\x04 \x01(\x0e2<.grpc.gateway.protoc_gen_openapiv2.options.SecurityScheme.In\x12L\n\x04flow\x18\x05 \x01(\x0e2>.grpc.gateway.protoc_gen_openapiv2.options.SecurityScheme.Flow\x12\x19\n\x11authorization_url\x18\x06 \x01(\t\x12\x11\n\ttoken_url\x18\x07 \x01(\t\x12A\n\x06scopes\x18\x08 \x01(\x0b21.grpc.gateway.protoc_gen_openapiv2.options.Scopes\x12]\n\nextensions\x18\t \x03(\x0b2I.grpc.gateway.protoc_gen_openapiv2.options.SecurityScheme.ExtensionsEntry\x1aI\n\x0fExtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b2\x16.google.protobuf.Value:\x028\x01"K\n\x04Type\x12\x10\n\x0cTYPE_INVALID\x10\x00\x12\x0e\n\nTYPE_BASIC\x10\x01\x12\x10\n\x0cTYPE_API_KEY\x10\x02\x12\x0f\n\x0bTYPE_OAUTH2\x10\x03"1\n\x02In\x12\x0e\n\nIN_INVALID\x10\x00\x12\x0c\n\x08IN_QUERY\x10\x01\x12\r\n\tIN_HEADER\x10\x02"j\n\x04Flow\x12\x10\n\x0cFLOW_INVALID\x10\x00\x12\x11\n\rFLOW_IMPLICIT\x10\x01\x12\x11\n\rFLOW_PASSWORD\x10\x02\x12\x14\n\x10FLOW_APPLICATION\x10\x03\x12\x14\n\x10FLOW_ACCESS_CODE\x10\x04"\xcd\x02\n\x13SecurityRequirement\x12u\n\x14security_requirement\x18\x01 \x03(\x0b2W.grpc.gateway.protoc_gen_openapiv2.options.SecurityRequirement.SecurityRequirementEntry\x1a)\n\x18SecurityRequirementValue\x12\r\n\x05scope\x18\x01 \x03(\t\x1a\x93\x01\n\x18SecurityRequirementEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12f\n\x05value\x18\x02 \x01(\x0b2W.grpc.gateway.protoc_gen_openapiv2.options.SecurityRequirement.SecurityRequirementValue:\x028\x01"\x83\x01\n\x06Scopes\x12K\n\x05scope\x18\x01 \x03(\x0b2<.grpc.gateway.protoc_gen_openapiv2.options.Scopes.ScopeEntry\x1a,\n\nScopeEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01*;\n\x06Scheme\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04HTTP\x10\x01\x12\t\n\x05HTTPS\x10\x02\x12\x06\n\x02WS\x10\x03\x12\x07\n\x03WSS\x10\x04BHZFgithub.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2/optionsb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protoc_gen_openapiv2.options.openapiv2_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'ZFgithub.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2/options'
    _globals['_SWAGGER_RESPONSESENTRY']._loaded_options = None
    _globals['_SWAGGER_RESPONSESENTRY']._serialized_options = b'8\x01'
    _globals['_SWAGGER_EXTENSIONSENTRY']._loaded_options = None
    _globals['_SWAGGER_EXTENSIONSENTRY']._serialized_options = b'8\x01'
    _globals['_OPERATION_RESPONSESENTRY']._loaded_options = None
    _globals['_OPERATION_RESPONSESENTRY']._serialized_options = b'8\x01'
    _globals['_OPERATION_EXTENSIONSENTRY']._loaded_options = None
    _globals['_OPERATION_EXTENSIONSENTRY']._serialized_options = b'8\x01'
    _globals['_RESPONSE_HEADERSENTRY']._loaded_options = None
    _globals['_RESPONSE_HEADERSENTRY']._serialized_options = b'8\x01'
    _globals['_RESPONSE_EXAMPLESENTRY']._loaded_options = None
    _globals['_RESPONSE_EXAMPLESENTRY']._serialized_options = b'8\x01'
    _globals['_RESPONSE_EXTENSIONSENTRY']._loaded_options = None
    _globals['_RESPONSE_EXTENSIONSENTRY']._serialized_options = b'8\x01'
    _globals['_INFO_EXTENSIONSENTRY']._loaded_options = None
    _globals['_INFO_EXTENSIONSENTRY']._serialized_options = b'8\x01'
    _globals['_SECURITYDEFINITIONS_SECURITYENTRY']._loaded_options = None
    _globals['_SECURITYDEFINITIONS_SECURITYENTRY']._serialized_options = b'8\x01'
    _globals['_SECURITYSCHEME_EXTENSIONSENTRY']._loaded_options = None
    _globals['_SECURITYSCHEME_EXTENSIONSENTRY']._serialized_options = b'8\x01'
    _globals['_SECURITYREQUIREMENT_SECURITYREQUIREMENTENTRY']._loaded_options = None
    _globals['_SECURITYREQUIREMENT_SECURITYREQUIREMENTENTRY']._serialized_options = b'8\x01'
    _globals['_SCOPES_SCOPEENTRY']._loaded_options = None
    _globals['_SCOPES_SCOPEENTRY']._serialized_options = b'8\x01'
    _globals['_SCHEME']._serialized_start = 5781
    _globals['_SCHEME']._serialized_end = 5840
    _globals['_SWAGGER']._serialized_start = 122
    _globals['_SWAGGER']._serialized_end = 983
    _globals['_SWAGGER_RESPONSESENTRY']._serialized_start = 789
    _globals['_SWAGGER_RESPONSESENTRY']._serialized_end = 890
    _globals['_SWAGGER_EXTENSIONSENTRY']._serialized_start = 892
    _globals['_SWAGGER_EXTENSIONSENTRY']._serialized_end = 965
    _globals['_OPERATION']._serialized_start = 986
    _globals['_OPERATION']._serialized_end = 1728
    _globals['_OPERATION_RESPONSESENTRY']._serialized_start = 789
    _globals['_OPERATION_RESPONSESENTRY']._serialized_end = 890
    _globals['_OPERATION_EXTENSIONSENTRY']._serialized_start = 892
    _globals['_OPERATION_EXTENSIONSENTRY']._serialized_end = 965
    _globals['_HEADER']._serialized_start = 1731
    _globals['_HEADER']._serialized_end = 1902
    _globals['_RESPONSE']._serialized_start = 1905
    _globals['_RESPONSE']._serialized_end = 2483
    _globals['_RESPONSE_HEADERSENTRY']._serialized_start = 2262
    _globals['_RESPONSE_HEADERSENTRY']._serialized_end = 2359
    _globals['_RESPONSE_EXAMPLESENTRY']._serialized_start = 2361
    _globals['_RESPONSE_EXAMPLESENTRY']._serialized_end = 2408
    _globals['_RESPONSE_EXTENSIONSENTRY']._serialized_start = 892
    _globals['_RESPONSE_EXTENSIONSENTRY']._serialized_end = 965
    _globals['_INFO']._serialized_start = 2486
    _globals['_INFO']._serialized_end = 2869
    _globals['_INFO_EXTENSIONSENTRY']._serialized_start = 892
    _globals['_INFO_EXTENSIONSENTRY']._serialized_end = 965
    _globals['_CONTACT']._serialized_start = 2871
    _globals['_CONTACT']._serialized_end = 2922
    _globals['_LICENSE']._serialized_start = 2924
    _globals['_LICENSE']._serialized_end = 2960
    _globals['_EXTERNALDOCUMENTATION']._serialized_start = 2962
    _globals['_EXTERNALDOCUMENTATION']._serialized_end = 3019
    _globals['_SCHEMA']._serialized_start = 3022
    _globals['_SCHEMA']._serialized_end = 3260
    _globals['_JSONSCHEMA']._serialized_start = 3263
    _globals['_JSONSCHEMA']._serialized_end = 4155
    _globals['_JSONSCHEMA_FIELDCONFIGURATION']._serialized_start = 3911
    _globals['_JSONSCHEMA_FIELDCONFIGURATION']._serialized_end = 3956
    _globals['_JSONSCHEMA_JSONSCHEMASIMPLETYPES']._serialized_start = 3958
    _globals['_JSONSCHEMA_JSONSCHEMASIMPLETYPES']._serialized_end = 4077
    _globals['_TAG']._serialized_start = 4157
    _globals['_TAG']._serialized_end = 4278
    _globals['_SECURITYDEFINITIONS']._serialized_start = 4281
    _globals['_SECURITYDEFINITIONS']._serialized_end = 4506
    _globals['_SECURITYDEFINITIONS_SECURITYENTRY']._serialized_start = 4400
    _globals['_SECURITYDEFINITIONS_SECURITYENTRY']._serialized_end = 4506
    _globals['_SECURITYSCHEME']._serialized_start = 4509
    _globals['_SECURITYSCHEME']._serialized_end = 5309
    _globals['_SECURITYSCHEME_EXTENSIONSENTRY']._serialized_start = 892
    _globals['_SECURITYSCHEME_EXTENSIONSENTRY']._serialized_end = 965
    _globals['_SECURITYSCHEME_TYPE']._serialized_start = 5075
    _globals['_SECURITYSCHEME_TYPE']._serialized_end = 5150
    _globals['_SECURITYSCHEME_IN']._serialized_start = 5152
    _globals['_SECURITYSCHEME_IN']._serialized_end = 5201
    _globals['_SECURITYSCHEME_FLOW']._serialized_start = 5203
    _globals['_SECURITYSCHEME_FLOW']._serialized_end = 5309
    _globals['_SECURITYREQUIREMENT']._serialized_start = 5312
    _globals['_SECURITYREQUIREMENT']._serialized_end = 5645
    _globals['_SECURITYREQUIREMENT_SECURITYREQUIREMENTVALUE']._serialized_start = 5454
    _globals['_SECURITYREQUIREMENT_SECURITYREQUIREMENTVALUE']._serialized_end = 5495
    _globals['_SECURITYREQUIREMENT_SECURITYREQUIREMENTENTRY']._serialized_start = 5498
    _globals['_SECURITYREQUIREMENT_SECURITYREQUIREMENTENTRY']._serialized_end = 5645
    _globals['_SCOPES']._serialized_start = 5648
    _globals['_SCOPES']._serialized_end = 5779
    _globals['_SCOPES_SCOPEENTRY']._serialized_start = 5735
    _globals['_SCOPES_SCOPEENTRY']._serialized_end = 5779