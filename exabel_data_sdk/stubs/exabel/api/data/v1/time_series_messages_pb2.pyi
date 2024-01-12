"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright (c) 2019-2022 Exabel AS. All rights reserved."""
import builtins
import collections.abc
from ..... import exabel
import google.protobuf.descriptor
import google.protobuf.duration_pb2
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import google.protobuf.wrappers_pb2
import google.type.decimal_pb2
import sys
import typing
if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class TimeSeries(google.protobuf.message.Message):
    """A time series resource in the Data API. All time series have one entity and one signal as its
    parents. As such, it can be referred to as both `{entity_name}/{signal_name}` and
    `{signal_name}/{entity_name}`. The first version is the canonical form.
    Some time series are provided by Exabel and their data cannot
    be retrieved via this API. They may still be listed in a `ListTimeSeries` request and be used on
    the Exabel platform.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    POINTS_FIELD_NUMBER: builtins.int
    READ_ONLY_FIELD_NUMBER: builtins.int
    UNITS_FIELD_NUMBER: builtins.int
    name: builtins.str
    'The resource name of the time series, for example\n    `entityTypes/ns1.type/entities/ns2.entities/signals/ns3.signal`.\n    An alternative name for the same time series is\n    `signals/ns3.signal/entityTypes/ns1.type/entities/ns2.entity`, but the former is the canonical\n    version which always will be returned by the server. The namespaces must be empty (being\n    global) or one of the predetermined namespaces the customer has access to. If ns2 is not empty,\n    it must be equals to ns3, and if ns1 is not empty, all three namespaces must be equal.\n    '

    @property
    def points(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___TimeSeriesPoint]:
        """List of time series data points. Data points are always returned by Exabel in chronological
        order (earliest first).
        """
    read_only: builtins.bool
    'Global time series and those from data sets that you subscribe to will be read-only.'

    @property
    def units(self) -> global___Units:
        """The units of this time series. Not all time series have known units, in which case this field
        is not present. Once set, only the `description` field of `units` may be updated.
        """

    def __init__(self, *, name: builtins.str | None=..., points: collections.abc.Iterable[global___TimeSeriesPoint] | None=..., read_only: builtins.bool | None=..., units: global___Units | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['units', b'units']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name', 'points', b'points', 'read_only', b'read_only', 'units', b'units']) -> None:
        ...
global___TimeSeries = TimeSeries

@typing_extensions.final
class TimeSeriesPoint(google.protobuf.message.Message):
    """A time series point of a time series."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TIME_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    KNOWN_TIME_FIELD_NUMBER: builtins.int

    @property
    def time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Timestamp of this data point, truncated to whole seconds."""

    @property
    def value(self) -> google.protobuf.wrappers_pb2.DoubleValue:
        """Value of this data point. Data points returned from the API always have values, but may be
        NaNs (Not a Number). Data points sent to the API may have no value, in which case they are
        marked as deleted at the specified `known_time`.
        """

    @property
    def known_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Known time of this data point."""

    def __init__(self, *, time: google.protobuf.timestamp_pb2.Timestamp | None=..., value: google.protobuf.wrappers_pb2.DoubleValue | None=..., known_time: google.protobuf.timestamp_pb2.Timestamp | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['known_time', b'known_time', 'time', b'time', 'value', b'value']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['known_time', b'known_time', 'time', b'time', 'value', b'value']) -> None:
        ...
global___TimeSeriesPoint = TimeSeriesPoint

@typing_extensions.final
class TimeSeriesView(google.protobuf.message.Message):
    """A view of the time series, specifying which parts of its data to return. The default view is
    to only return the name of the time series.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TIME_RANGE_FIELD_NUMBER: builtins.int
    KNOWN_TIME_FIELD_NUMBER: builtins.int

    @property
    def time_range(self) -> exabel.api.time.time_range_pb2.TimeRange:
        """The time range of points to return. If the time series is provided by Exabel, this field will
        be treated as not set. If not set, no points will be returned. If set, but empty, all points
        will be returned.
        """

    @property
    def known_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Specifies that the time series should be returned as it was known at this time (in the past).
        Data points known after this time are disregarded. If not set, the latest data points are
        returned.
        """

    def __init__(self, *, time_range: exabel.api.time.time_range_pb2.TimeRange | None=..., known_time: google.protobuf.timestamp_pb2.Timestamp | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['known_time', b'known_time', 'time_range', b'time_range']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['known_time', b'known_time', 'time_range', b'time_range']) -> None:
        ...
global___TimeSeriesView = TimeSeriesView

@typing_extensions.final
class DefaultKnownTime(google.protobuf.message.Message):
    """A default known time specification to use when creating or updating time series. If any inserted
    values has a value for its known_time, that value is used instead.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CURRENT_TIME_FIELD_NUMBER: builtins.int
    KNOWN_TIME_FIELD_NUMBER: builtins.int
    TIME_OFFSET_FIELD_NUMBER: builtins.int
    current_time: builtins.bool
    'Specifies the current system time as the default known time for all inserted data points.'

    @property
    def known_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Specifies a specific timestamp as the default known time for all inserted data points."""

    @property
    def time_offset(self) -> google.protobuf.duration_pb2.Duration:
        """Specifies a time offset from each data point's timestamp to be its default known time."""

    def __init__(self, *, current_time: builtins.bool | None=..., known_time: google.protobuf.timestamp_pb2.Timestamp | None=..., time_offset: google.protobuf.duration_pb2.Duration | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['current_time', b'current_time', 'known_time', b'known_time', 'specification', b'specification', 'time_offset', b'time_offset']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['current_time', b'current_time', 'known_time', b'known_time', 'specification', b'specification', 'time_offset', b'time_offset']) -> None:
        ...

    def WhichOneof(self, oneof_group: typing_extensions.Literal['specification', b'specification']) -> typing_extensions.Literal['current_time', 'known_time', 'time_offset'] | None:
        ...
global___DefaultKnownTime = DefaultKnownTime

@typing_extensions.final
class Units(google.protobuf.message.Message):
    """The units of a time series. Not all time series have known units, in which case its `units`
    field is not present. If present, but empty, the unit of the time series is known to be
    dimensionless and unscaled.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    UNITS_FIELD_NUMBER: builtins.int
    MULTIPLIER_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int

    @property
    def units(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Unit]:
        """The product of all individual unit parts of this unit. For instance, if a time series measures
        speed and is given in meters per second, it would have one unit
        `{ dimension: DIMENSION_LENGTH, unit: 'm' }` and one unit
        `{ dimension: DIMENSION_TIME, unit: 's', exponent: -1 }. And if a time series measures a
        monetary amount and is specified in United States dollars, it would have the single unit
        `{ dimension: DIMENSION_CURRENCY, unit: 'USD' }`.
        """

    @property
    def multiplier(self) -> google.type.decimal_pb2.Decimal:
        """The multiplier of the time series, with default value "1". For instance, if the time series is
        measured in millions, the multiplier would be "1000000" or "1e6", or if the time series is
        measured in percent, but given as values from 0 to 100, the multiplier would be "0.01".
        """
    description: builtins.str
    'Optionally a more detailed description of the units of this time series,\n    for instance "Number of customers" or "Gross value in millions (EUR)".\n    '

    def __init__(self, *, units: collections.abc.Iterable[global___Unit] | None=..., multiplier: google.type.decimal_pb2.Decimal | None=..., description: builtins.str | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['multiplier', b'multiplier']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['description', b'description', 'multiplier', b'multiplier', 'units', b'units']) -> None:
        ...
global___Units = Units

@typing_extensions.final
class Unit(google.protobuf.message.Message):
    """An individual unit, measuring one dimension."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Dimension:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _DimensionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Unit._Dimension.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        DIMENSION_UNKNOWN: Unit._Dimension.ValueType
        "The dimension of this unit is unknown, but may be inferred from the unit's symbol."
        DIMENSION_CURRENCY: Unit._Dimension.ValueType
        'The dimension is a monetary currency. A unit of this dimension must be one of the ISO-4217\n        three letter currency codes.\n        '
        DIMENSION_MASS: Unit._Dimension.ValueType
        'The dimension is a mass. The SI unit of mass is "kg", but other units may also be used.'
        DIMENSION_LENGTH: Unit._Dimension.ValueType
        'The dimension is a one dimensional size. The SI unit of length is "m", but other units may\n        also be used.\n        '
        DIMENSION_TIME: Unit._Dimension.ValueType
        'The dimension is an amount of time. The SI unit of time is "s", but other units may also be\n        used.\n        '

    class Dimension(_Dimension, metaclass=_DimensionEnumTypeWrapper):
        """The supported dimensions in the Exabel platform."""
    DIMENSION_UNKNOWN: Unit.Dimension.ValueType
    "The dimension of this unit is unknown, but may be inferred from the unit's symbol."
    DIMENSION_CURRENCY: Unit.Dimension.ValueType
    'The dimension is a monetary currency. A unit of this dimension must be one of the ISO-4217\n    three letter currency codes.\n    '
    DIMENSION_MASS: Unit.Dimension.ValueType
    'The dimension is a mass. The SI unit of mass is "kg", but other units may also be used.'
    DIMENSION_LENGTH: Unit.Dimension.ValueType
    'The dimension is a one dimensional size. The SI unit of length is "m", but other units may\n    also be used.\n    '
    DIMENSION_TIME: Unit.Dimension.ValueType
    'The dimension is an amount of time. The SI unit of time is "s", but other units may also be\n    used.\n    '
    DIMENSION_FIELD_NUMBER: builtins.int
    UNIT_FIELD_NUMBER: builtins.int
    EXPONENT_FIELD_NUMBER: builtins.int
    dimension: global___Unit.Dimension.ValueType
    'The dimension of this unit.'
    unit: builtins.str
    'The short hand symbol of a dimension of this unit, for instance "m" or "EUR".'
    exponent: builtins.int
    "The exponent (power) of this unit. It can be positive or negative, but if it is 0, the unit's\n    exponent defaults to the value 1.\n    "

    def __init__(self, *, dimension: global___Unit.Dimension.ValueType | None=..., unit: builtins.str | None=..., exponent: builtins.int | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['dimension', b'dimension', 'exponent', b'exponent', 'unit', b'unit']) -> None:
        ...
global___Unit = Unit