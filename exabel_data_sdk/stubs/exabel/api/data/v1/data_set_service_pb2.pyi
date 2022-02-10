"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from exabel_data_sdk.stubs.exabel.api.data.v1.data_set_messages_pb2 import (
    DataSet as exabel___api___data___v1___data_set_messages_pb2___DataSet,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.field_mask_pb2 import (
    FieldMask as google___protobuf___field_mask_pb2___FieldMask,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    Optional as typing___Optional,
    Text as typing___Text,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

class ListDataSetsRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    def __init__(self,
        ) -> None: ...
type___ListDataSetsRequest = ListDataSetsRequest

class ListDataSetsResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def data_sets(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[exabel___api___data___v1___data_set_messages_pb2___DataSet]: ...

    def __init__(self,
        *,
        data_sets : typing___Optional[typing___Iterable[exabel___api___data___v1___data_set_messages_pb2___DataSet]] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"data_sets",b"data_sets"]) -> None: ...
type___ListDataSetsResponse = ListDataSetsResponse

class GetDataSetRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    name: typing___Text = ...

    def __init__(self,
        *,
        name : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"name",b"name"]) -> None: ...
type___GetDataSetRequest = GetDataSetRequest

class CreateDataSetRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def data_set(self) -> exabel___api___data___v1___data_set_messages_pb2___DataSet: ...

    def __init__(self,
        *,
        data_set : typing___Optional[exabel___api___data___v1___data_set_messages_pb2___DataSet] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"data_set",b"data_set"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"data_set",b"data_set"]) -> None: ...
type___CreateDataSetRequest = CreateDataSetRequest

class UpdateDataSetRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    allow_missing: builtin___bool = ...

    @property
    def data_set(self) -> exabel___api___data___v1___data_set_messages_pb2___DataSet: ...

    @property
    def update_mask(self) -> google___protobuf___field_mask_pb2___FieldMask: ...

    def __init__(self,
        *,
        data_set : typing___Optional[exabel___api___data___v1___data_set_messages_pb2___DataSet] = None,
        update_mask : typing___Optional[google___protobuf___field_mask_pb2___FieldMask] = None,
        allow_missing : typing___Optional[builtin___bool] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"data_set",b"data_set",u"update_mask",b"update_mask"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"allow_missing",b"allow_missing",u"data_set",b"data_set",u"update_mask",b"update_mask"]) -> None: ...
type___UpdateDataSetRequest = UpdateDataSetRequest

class DeleteDataSetRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    name: typing___Text = ...

    def __init__(self,
        *,
        name : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"name",b"name"]) -> None: ...
type___DeleteDataSetRequest = DeleteDataSetRequest
