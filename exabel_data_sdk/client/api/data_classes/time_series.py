from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence

import numpy as np
import pandas as pd
from dateutil import tz

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import TimeSeries as ProtoTimeSeries
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import TimeSeriesPoint
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import Unit as ProtoUnit
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import Units as ProtoUnits


class Dimension(Enum):
    """Enum representing the dimension of a unit."""

    DIMENSION_UNKNOWN = ProtoUnit.Dimension.DIMENSION_UNKNOWN
    DIMENSION_CURRENCY = ProtoUnit.Dimension.DIMENSION_CURRENCY
    DIMENSION_MASS = ProtoUnit.Dimension.DIMENSION_MASS
    DIMENSION_LENGTH = ProtoUnit.Dimension.DIMENSION_LENGTH
    DIMENSION_TIME = ProtoUnit.Dimension.DIMENSION_TIME
    DIMENSION_RATIO = ProtoUnit.Dimension.DIMENSION_RATIO

    @classmethod
    def from_string(cls, dimension: str) -> Dimension:
        """Get the Dimension enum from a string."""
        key = f"DIMENSION_{dimension.upper()}"
        try:
            return cls[key]
        except KeyError as e:
            raise ValueError(
                f"Unknown dimension: {dimension}. "
                + "Supported values are: unknown, currency, mass, length, time, and ratio."
            ) from e


DEFAULT_DIMENSION = Dimension.DIMENSION_UNKNOWN


def _invalid_time_series_name(name: str) -> ValueError:
    return ValueError(
        f"Unable to parse time series name: {name}. Should contain 6 parts on the canonical form: "
        "entityTypes/<entityType>/entities/<entity>/signals/<signal> or the alternative form: "
        "signals/<signal>/entityTypes/<entityType>/entities/<entity>"
    )


@dataclass(frozen=True)
class TimeSeriesResourceName:
    """Represents a time series resource name."""

    entity_type: str
    entity: str
    signal: str

    @property
    def entity_name(self) -> str:
        """Get the entity name."""
        return f"entityTypes/{self.entity_type}/entities/{self.entity}"

    @property
    def signal_name(self) -> str:
        """Get the signal name."""
        return f"signals/{self.signal}"

    @property
    def canonical_name(self) -> str:
        """The canonical name of the time series."""
        return f"{self.entity_name}/{self.signal_name}"

    @classmethod
    def from_string(cls, name: str) -> TimeSeriesResourceName:
        """Create a time series resource name from a string."""
        ts_name_parts = name.split("/")
        if len(ts_name_parts) != 6:
            raise _invalid_time_series_name(name)
        if (ts_name_parts[0], ts_name_parts[2], ts_name_parts[4]) == (
            "entityTypes",
            "entities",
            "signals",
        ):
            entity_type = ts_name_parts[1]
            entity = ts_name_parts[3]
            signal = ts_name_parts[5]
        elif (ts_name_parts[0], ts_name_parts[2], ts_name_parts[4]) == (
            "signals",
            "entityTypes",
            "entities",
        ):
            signal = ts_name_parts[1]
            entity_type = ts_name_parts[3]
            entity = ts_name_parts[5]
        else:
            raise _invalid_time_series_name(name)
        return cls(entity_type, entity, signal)


@dataclass
class TimeSeries:
    """
    A time series resource in the Data API.

    Attributes:
        series:     A pandas Series where the name attribute is the canonical name of the
                    time series.
        units:      Units for the time series. A time series can have a single unit or a
                    combination of units. For example, a time series can have the unit
                    USD per month, which is a combination of the units USD and month.
                    If None, the units are unknown.
    """

    series: pd.Series
    units: Optional[Units] = None

    @property
    def name(self) -> str:
        """The canonical name of the time series."""
        return self.series.name

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the time series."""
        self.series.name = name

    @staticmethod
    def from_proto(time_series: ProtoTimeSeries) -> TimeSeries:
        """Create a TimeSeries from the given protobuf TimeSeries."""
        return TimeSeries(
            series=TimeSeries._time_series_points_to_series(time_series.points, time_series.name),
            units=Units.from_proto(time_series.units) if time_series.HasField("units") else None,
        )

    def to_proto(self) -> ProtoTimeSeries:
        """Create a protobuf TimeSeries from this TimeSeries."""
        return ProtoTimeSeries(
            name=self.series.name,
            points=self._series_to_time_series_points(self.series),
            units=self.units.to_proto() if self.units else None,
        )

    @staticmethod
    def _time_series_points_to_series(
        points: Sequence[TimeSeriesPoint], name: Optional[str] = None
    ) -> pd.Series:
        """Convert a sequence of TimeSeriesPoint to a pandas Series."""
        known_time = False
        for point in points:
            if point.HasField("known_time"):
                known_time = True
                break

        if known_time:
            index = pd.MultiIndex.from_tuples(
                zip(
                    TimeSeries._datetime_index([x.time.ToNanoseconds() for x in points]),
                    TimeSeries._datetime_index(
                        [x.known_time.ToNanoseconds() for x in points if x.known_time]
                    ),
                ),
            )
        else:
            index = TimeSeries._datetime_index([x.time.ToNanoseconds() for x in points])

        return pd.Series(
            map(lambda x: x.value.value, points),
            index,
            name=name,
        )

    @staticmethod
    def _series_to_time_series_points(series: pd.Series) -> Sequence[TimeSeriesPoint]:
        """Convert a pandas Series to a sequence of TimeSeriesPoint."""
        points = []
        for index, value in series.items():
            # Logic from _pandas_timestamp_to_proto has been inlined here for performance.
            point = TimeSeriesPoint()
            if isinstance(index, tuple):
                # (timestamp, known_time)
                if len(index) != 2:
                    raise ValueError(
                        "A time series with a MultiIndex is expected to have exactly "
                        f"two elements: (timestamp, known_time), but got {index}"
                    )
                timestamp = index[0]
                point.known_time.seconds = index[1].value // 1_000_000_000
            else:
                timestamp = index
            if timestamp is pd.NaT:
                raise ValueError("Timestamp must be set")
            point.time.seconds = timestamp.value // 1_000_000_000
            point.value.value = value
            points.append(point)
        return points

    @staticmethod
    def _datetime_index(nanoseconds: Sequence[int]) -> pd.DatetimeIndex:
        return pd.DatetimeIndex(np.array(nanoseconds).astype("datetime64[ns]"), tz=tz.tzutc())

    def __repr__(self) -> str:
        return f"{self.series}\n{self.units}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TimeSeries):
            return False
        return self.series.equals(other.series) and self.units == other.units


@dataclass
class Units:
    """
    A units resource in the Data API.

    Attributes:
        units:          A list of units that are multiplied together to get the final unit.
        description:    A description of the units. E.g. "ratio" or "percentage".
    """

    units: Sequence[Unit] = field(default_factory=list)
    description: Optional[str] = None

    @staticmethod
    def from_proto(proto_units: ProtoUnits) -> Units:
        """Create a Units from the given protobuf Units."""
        return Units(
            units=[Unit.from_proto(unit) for unit in proto_units.units],
            description=proto_units.description or None,
        )

    def to_proto(self) -> ProtoUnits:
        """Create a protobuf Units from this Units."""
        return ProtoUnits(
            units=[unit.to_proto() for unit in self.units],
            description=self.description,
        )


@dataclass
class Unit:
    """
    A unit resource in the Data API.

    Attributes:
        dimension:  The dimension of the unit. E.g. "DIMENSION_CURRENCY" for currency.
        unit:       The unit. E.g. "USD" or "EUR" for currency.
        exponent:   The exponent of the unit. Equal to 1 if it is in the numerator and
                    -1 if it is in the denominator. If None, the exponent is defaulted to 1.
    """

    dimension: Dimension
    unit: Optional[str] = None
    exponent: Optional[int] = None

    @staticmethod
    def from_proto(proto_unit: ProtoUnit) -> Unit:
        """Create a Unit from the given protobuf Unit."""
        return Unit(
            dimension=Dimension(proto_unit.dimension),
            unit=proto_unit.unit or None,
            exponent=proto_unit.exponent or None,
        )

    def to_proto(self) -> ProtoUnit:
        """Create a protobuf Unit from this Unit."""
        return ProtoUnit(
            dimension=self.dimension.value,
            unit=self.unit,
            exponent=self.exponent,
        )
