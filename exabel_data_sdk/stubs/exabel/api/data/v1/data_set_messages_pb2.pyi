"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright (c) 2019-2024 Exabel AS. All rights reserved."""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class DataSet(google.protobuf.message.Message):
    """A data set resource in the Data API."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    LEGACY_NAME_FIELD_NUMBER: builtins.int
    DISPLAY_NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    SIGNALS_FIELD_NUMBER: builtins.int
    DERIVED_SIGNALS_FIELD_NUMBER: builtins.int
    HIGHLIGHTED_SIGNALS_FIELD_NUMBER: builtins.int
    READ_ONLY_FIELD_NUMBER: builtins.int
    name: builtins.str
    'Unique resource name of the data set, e.g. `dataSets/namespace.dataSetIdentifier`.\n    The namespace must be one of the predetermined namespaces the customer has access to.\n    The data set identifier must match the regex `\\w[\\w-]{0,63}`.\n    '
    legacy_name: builtins.str
    'The legacy resource name of the data set. Only some data sets have legacy names, and the format\n    is `dataSets/n`, where n is a positive integer. The legacy name cannot be changed here, but\n    must be changed via the management API.\n    '
    display_name: builtins.str
    'Used when showing the data set in the Exabel app. Required when creating a data set.'
    description: builtins.str
    'This is currently not used in the Exabel app, but may be in future.'
    read_only: builtins.bool
    'Data sets that you subscribe to will be read-only.'

    @property
    def signals(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """List of signals comprising the data set. Signals are represented by their resource names,
        e.g. `signals/namespace.signalIdentifier`.
        """

    @property
    def derived_signals(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """List of derived signals in the data set, in decreasing order of "importance". Derived signals
        are represented by their resource names, e.g. `derivedSignals/42`.
        """

    @property
    def highlighted_signals(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """List of signals that are highlighted in this data set."""

    def __init__(self, *, name: builtins.str | None=..., legacy_name: builtins.str | None=..., display_name: builtins.str | None=..., description: builtins.str | None=..., signals: collections.abc.Iterable[builtins.str] | None=..., derived_signals: collections.abc.Iterable[builtins.str] | None=..., highlighted_signals: collections.abc.Iterable[builtins.str] | None=..., read_only: builtins.bool | None=...) -> None:
        ...

    def ClearField(self, field_name: typing.Literal['derived_signals', b'derived_signals', 'description', b'description', 'display_name', b'display_name', 'highlighted_signals', b'highlighted_signals', 'legacy_name', b'legacy_name', 'name', b'name', 'read_only', b'read_only', 'signals', b'signals']) -> None:
        ...
global___DataSet = DataSet