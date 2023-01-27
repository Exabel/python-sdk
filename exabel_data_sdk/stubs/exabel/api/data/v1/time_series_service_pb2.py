"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....exabel.api.data.v1 import time_series_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2
from .....exabel.api.time import time_range_pb2 as exabel_dot_api_dot_time_dot_time__range__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import visibility_pb2 as google_dot_api_dot_visibility__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,exabel/api/data/v1/time_series_service.proto\x12\x12exabel.api.data.v1\x1a-exabel/api/data/v1/time_series_messages.proto\x1a exabel/api/time/time_range.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/api/visibility.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"l\n\x15ListTimeSeriesRequest\x12,\n\x06parent\x18\x01 \x01(\tB\x1c\xe0A\x02\x92A\x16\xca>\x13\xfa\x02\x10timeSeriesParent\x12\x11\n\tpage_size\x18\x02 \x01(\x05\x12\x12\n\npage_token\x18\x03 \x01(\t"z\n\x16ListTimeSeriesResponse\x123\n\x0btime_series\x18\x01 \x03(\x0b2\x1e.exabel.api.data.v1.TimeSeries\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"r\n\x14GetTimeSeriesRequest\x12(\n\x04name\x18\x01 \x01(\tB\x1a\xe0A\x02\x92A\x14\xca>\x11\xfa\x02\x0etimeSeriesName\x120\n\x04view\x18\x02 \x01(\x0b2".exabel.api.data.v1.TimeSeriesView"\xdb\x01\n\x17CreateTimeSeriesRequest\x128\n\x0btime_series\x18\x01 \x01(\x0b2\x1e.exabel.api.data.v1.TimeSeriesB\x03\xe0A\x02\x120\n\x04view\x18\x02 \x01(\x0b2".exabel.api.data.v1.TimeSeriesView\x12@\n\x12default_known_time\x18\x03 \x01(\x0b2$.exabel.api.data.v1.DefaultKnownTime\x12\x12\n\ncreate_tag\x18\x04 \x01(\x08"\xf2\x01\n\x17UpdateTimeSeriesRequest\x128\n\x0btime_series\x18\x01 \x01(\x0b2\x1e.exabel.api.data.v1.TimeSeriesB\x03\xe0A\x02\x120\n\x04view\x18\x02 \x01(\x0b2".exabel.api.data.v1.TimeSeriesView\x12@\n\x12default_known_time\x18\x03 \x01(\x0b2$.exabel.api.data.v1.DefaultKnownTime\x12\x15\n\rallow_missing\x18\x04 \x01(\x08\x12\x12\n\ncreate_tag\x18\x05 \x01(\x08"\xd0\x01\n\x17ImportTimeSeriesRequest\x12\x13\n\x06parent\x18\x01 \x01(\tB\x03\xe0A\x02\x123\n\x0btime_series\x18\x02 \x03(\x0b2\x1e.exabel.api.data.v1.TimeSeries\x12@\n\x12default_known_time\x18\x03 \x01(\x0b2$.exabel.api.data.v1.DefaultKnownTime\x12\x15\n\rallow_missing\x18\x04 \x01(\x08\x12\x12\n\ncreate_tag\x18\x05 \x01(\x08"\x1a\n\x18ImportTimeSeriesResponse"C\n\x17DeleteTimeSeriesRequest\x12(\n\x04name\x18\x01 \x01(\tB\x1a\xe0A\x02\x92A\x14\xca>\x11\xfa\x02\x0etimeSeriesName"\x7f\n"BatchDeleteTimeSeriesPointsRequest\x12(\n\x04name\x18\x01 \x01(\tB\x1a\xe0A\x02\x92A\x14\xca>\x11\xfa\x02\x0etimeSeriesName\x12/\n\x0btime_ranges\x18\x02 \x03(\x0b2\x1a.exabel.api.time.TimeRange2\x80\x0e\n\x11TimeSeriesService\x12\xdb\x01\n\x0eListTimeSeries\x12).exabel.api.data.v1.ListTimeSeriesRequest\x1a*.exabel.api.data.v1.ListTimeSeriesResponse"r\x82\xd3\xe4\x93\x02W\x120/v1/{parent=entityTypes/*/entities/*}/timeSeriesZ#\x12!/v1/{parent=signals/*}/timeSeries\x92A\x12\x12\x10List time series\x12\xd5\x01\n\rGetTimeSeries\x12(.exabel.api.data.v1.GetTimeSeriesRequest\x1a\x1e.exabel.api.data.v1.TimeSeries"z\x82\xd3\xe4\x93\x02`\x12-/v1/{name=entityTypes/*/entities/*/signals/*}Z/\x12-/v1/{name=signals/*/entityTypes/*/entities/*}\x92A\x11\x12\x0fGet time series\x12\x92\x02\n\x10CreateTimeSeries\x12+.exabel.api.data.v1.CreateTimeSeriesRequest\x1a\x1e.exabel.api.data.v1.TimeSeries"\xb0\x01\x82\xd3\xe4\x93\x02\x92\x01"9/v1/{time_series.name=entityTypes/*/entities/*/signals/*}:\x0btime_seriesZH"9/v1/{time_series.name=signals/*/entityTypes/*/entities/*}:\x0btime_series\x92A\x14\x12\x12Create time series\x12\x92\x02\n\x10UpdateTimeSeries\x12+.exabel.api.data.v1.UpdateTimeSeriesRequest\x1a\x1e.exabel.api.data.v1.TimeSeries"\xb0\x01\x82\xd3\xe4\x93\x02\x92\x0129/v1/{time_series.name=entityTypes/*/entities/*/signals/*}:\x0btime_seriesZH29/v1/{time_series.name=signals/*/entityTypes/*/entities/*}:\x0btime_series\x92A\x14\x12\x12Update time series\x12\xf8\x01\n\x10ImportTimeSeries\x12+.exabel.api.data.v1.ImportTimeSeriesRequest\x1a,.exabel.api.data.v1.ImportTimeSeriesResponse"\x88\x01\x82\xd3\xe4\x93\x02k"7/v1/{parent=entityTypes/*/entities/*}/timeSeries:import:\x01*Z-"(/v1/{parent=signals/*}/timeSeries:import:\x01*\x92A\x14\x12\x12Import time series\x12\xd6\x01\n\x10DeleteTimeSeries\x12+.exabel.api.data.v1.DeleteTimeSeriesRequest\x1a\x16.google.protobuf.Empty"}\x82\xd3\xe4\x93\x02`*-/v1/{name=entityTypes/*/entities/*/signals/*}Z/*-/v1/{name=signals/*/entityTypes/*/entities/*}\x92A\x14\x12\x12Delete time series\x12\xb6\x02\n\x1bBatchDeleteTimeSeriesPoints\x126.exabel.api.data.v1.BatchDeleteTimeSeriesPointsRequest\x1a\x16.google.protobuf.Empty"\xc6\x01\xfa\xd2\xe4\x93\x02\n\x12\x08INTERNAL\x82\xd3\xe4\x93\x02\x8c\x01"@/v1/{name=entityTypes/*/entities/*/signals/*}/points:batchDelete:\x01*ZE"@/v1/{name=signals/*/entityTypes/*/entities/*}/points:batchDelete:\x01*\x92A \x12\x1eDelete time series data pointsBJ\n\x16com.exabel.api.data.v1B\x16TimeSeriesServiceProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.time_series_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x16TimeSeriesServiceProtoP\x01Z\x16exabel.com/api/data/v1'
    _LISTTIMESERIESREQUEST.fields_by_name['parent']._options = None
    _LISTTIMESERIESREQUEST.fields_by_name['parent']._serialized_options = b'\xe0A\x02\x92A\x16\xca>\x13\xfa\x02\x10timeSeriesParent'
    _GETTIMESERIESREQUEST.fields_by_name['name']._options = None
    _GETTIMESERIESREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\x14\xca>\x11\xfa\x02\x0etimeSeriesName'
    _CREATETIMESERIESREQUEST.fields_by_name['time_series']._options = None
    _CREATETIMESERIESREQUEST.fields_by_name['time_series']._serialized_options = b'\xe0A\x02'
    _UPDATETIMESERIESREQUEST.fields_by_name['time_series']._options = None
    _UPDATETIMESERIESREQUEST.fields_by_name['time_series']._serialized_options = b'\xe0A\x02'
    _IMPORTTIMESERIESREQUEST.fields_by_name['parent']._options = None
    _IMPORTTIMESERIESREQUEST.fields_by_name['parent']._serialized_options = b'\xe0A\x02'
    _DELETETIMESERIESREQUEST.fields_by_name['name']._options = None
    _DELETETIMESERIESREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\x14\xca>\x11\xfa\x02\x0etimeSeriesName'
    _BATCHDELETETIMESERIESPOINTSREQUEST.fields_by_name['name']._options = None
    _BATCHDELETETIMESERIESPOINTSREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\x14\xca>\x11\xfa\x02\x0etimeSeriesName'
    _TIMESERIESSERVICE.methods_by_name['ListTimeSeries']._options = None
    _TIMESERIESSERVICE.methods_by_name['ListTimeSeries']._serialized_options = b'\x82\xd3\xe4\x93\x02W\x120/v1/{parent=entityTypes/*/entities/*}/timeSeriesZ#\x12!/v1/{parent=signals/*}/timeSeries\x92A\x12\x12\x10List time series'
    _TIMESERIESSERVICE.methods_by_name['GetTimeSeries']._options = None
    _TIMESERIESSERVICE.methods_by_name['GetTimeSeries']._serialized_options = b'\x82\xd3\xe4\x93\x02`\x12-/v1/{name=entityTypes/*/entities/*/signals/*}Z/\x12-/v1/{name=signals/*/entityTypes/*/entities/*}\x92A\x11\x12\x0fGet time series'
    _TIMESERIESSERVICE.methods_by_name['CreateTimeSeries']._options = None
    _TIMESERIESSERVICE.methods_by_name['CreateTimeSeries']._serialized_options = b'\x82\xd3\xe4\x93\x02\x92\x01"9/v1/{time_series.name=entityTypes/*/entities/*/signals/*}:\x0btime_seriesZH"9/v1/{time_series.name=signals/*/entityTypes/*/entities/*}:\x0btime_series\x92A\x14\x12\x12Create time series'
    _TIMESERIESSERVICE.methods_by_name['UpdateTimeSeries']._options = None
    _TIMESERIESSERVICE.methods_by_name['UpdateTimeSeries']._serialized_options = b'\x82\xd3\xe4\x93\x02\x92\x0129/v1/{time_series.name=entityTypes/*/entities/*/signals/*}:\x0btime_seriesZH29/v1/{time_series.name=signals/*/entityTypes/*/entities/*}:\x0btime_series\x92A\x14\x12\x12Update time series'
    _TIMESERIESSERVICE.methods_by_name['ImportTimeSeries']._options = None
    _TIMESERIESSERVICE.methods_by_name['ImportTimeSeries']._serialized_options = b'\x82\xd3\xe4\x93\x02k"7/v1/{parent=entityTypes/*/entities/*}/timeSeries:import:\x01*Z-"(/v1/{parent=signals/*}/timeSeries:import:\x01*\x92A\x14\x12\x12Import time series'
    _TIMESERIESSERVICE.methods_by_name['DeleteTimeSeries']._options = None
    _TIMESERIESSERVICE.methods_by_name['DeleteTimeSeries']._serialized_options = b'\x82\xd3\xe4\x93\x02`*-/v1/{name=entityTypes/*/entities/*/signals/*}Z/*-/v1/{name=signals/*/entityTypes/*/entities/*}\x92A\x14\x12\x12Delete time series'
    _TIMESERIESSERVICE.methods_by_name['BatchDeleteTimeSeriesPoints']._options = None
    _TIMESERIESSERVICE.methods_by_name['BatchDeleteTimeSeriesPoints']._serialized_options = b'\xfa\xd2\xe4\x93\x02\n\x12\x08INTERNAL\x82\xd3\xe4\x93\x02\x8c\x01"@/v1/{name=entityTypes/*/entities/*/signals/*}/points:batchDelete:\x01*ZE"@/v1/{name=signals/*/entityTypes/*/entities/*}/points:batchDelete:\x01*\x92A \x12\x1eDelete time series data points'
    _LISTTIMESERIESREQUEST._serialized_start = 318
    _LISTTIMESERIESREQUEST._serialized_end = 426
    _LISTTIMESERIESRESPONSE._serialized_start = 428
    _LISTTIMESERIESRESPONSE._serialized_end = 550
    _GETTIMESERIESREQUEST._serialized_start = 552
    _GETTIMESERIESREQUEST._serialized_end = 666
    _CREATETIMESERIESREQUEST._serialized_start = 669
    _CREATETIMESERIESREQUEST._serialized_end = 888
    _UPDATETIMESERIESREQUEST._serialized_start = 891
    _UPDATETIMESERIESREQUEST._serialized_end = 1133
    _IMPORTTIMESERIESREQUEST._serialized_start = 1136
    _IMPORTTIMESERIESREQUEST._serialized_end = 1344
    _IMPORTTIMESERIESRESPONSE._serialized_start = 1346
    _IMPORTTIMESERIESRESPONSE._serialized_end = 1372
    _DELETETIMESERIESREQUEST._serialized_start = 1374
    _DELETETIMESERIESREQUEST._serialized_end = 1441
    _BATCHDELETETIMESERIESPOINTSREQUEST._serialized_start = 1443
    _BATCHDELETETIMESERIESPOINTSREQUEST._serialized_end = 1570
    _TIMESERIESSERVICE._serialized_start = 1573
    _TIMESERIESSERVICE._serialized_end = 3365