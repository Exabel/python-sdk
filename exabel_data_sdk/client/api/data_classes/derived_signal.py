from enum import Enum
from typing import Optional

from google.protobuf.wrappers_pb2 import Int32Value

from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    DerivedSignal as ProtoDerivedSignal,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    DerivedSignalMetadata as ProtoDerivedSignalMetadata,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    DerivedSignalType as ProtoDerivedSignalType,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    DerivedSignalUnit as ProtoDerivedSignalUnit,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.signal_messages_pb2 import (
    DerivedSignal as ProtoDataApiDerivedSignal,
)
from exabel_data_sdk.stubs.exabel.api.math.aggregation_pb2 import Aggregation
from exabel_data_sdk.stubs.exabel.api.math.change_pb2 import Change


class DerivedSignalType(Enum):
    """Enum representing the type of a signal."""

    # The signal is a normal derived signal, represented by an editable expression and label.
    DERIVED_SIGNAL = ProtoDerivedSignalType.DERIVED_SIGNAL
    # A signal with time series uploaded through the app's file upload.
    # The expression refers to a raw signal and cannot be modified.
    FILE_UPLOADED_SIGNAL = ProtoDerivedSignalType.FILE_UPLOADED_SIGNAL
    # A signal with company time series uploaded through the app's file upload.
    # The expression refers to a raw signal and cannot be modified.
    FILE_UPLOADED_COMPANY_SIGNAL = ProtoDerivedSignalType.FILE_UPLOADED_COMPANY_SIGNAL
    # A persisted signal.
    # The expression refers to a raw signal and cannot be modified.
    PERSISTED_SIGNAL = ProtoDerivedSignalType.PERSISTED_SIGNAL


class DerivedSignalUnit(Enum):
    """Enum representing the unit of a derived signal."""

    # The signal has not been assigned a unit.
    DERIVED_SIGNAL_UNIT_INVALID = ProtoDerivedSignalUnit.DERIVED_SIGNAL_UNIT_INVALID
    # The signal represents normal floating point numbers.
    NUMBER = ProtoDerivedSignalUnit.NUMBER
    # The signal represents a ratio, typically with values in the interval [0, 1].
    # Values will be displayed as a percentage.
    RATIO = ProtoDerivedSignalUnit.RATIO
    # The signal represents a difference in a ratio.
    # Values will be displayed as percentage points.
    RATIO_DIFFERENCE = ProtoDerivedSignalUnit.RATIO_DIFFERENCE


class DerivedSignalMetaData:
    """
    Metadata of a derived signal.

    Attributes:
        unit:                   Unit of the signal.
        decimals:               Number of decimals to use when displaying signal values.
        signal_type:            Type of the signal.
        downsampling_method:    The default downsampling method to use when resampling.
        change:                 The method used to calculate changes in this signal.
    """

    def __init__(
        self,
        unit: DerivedSignalUnit = DerivedSignalUnit.NUMBER,
        decimals: Optional[int] = None,
        signal_type: DerivedSignalType = DerivedSignalType.DERIVED_SIGNAL,
        downsampling_method: Optional[Aggregation.ValueType] = None,
        change: Optional[Change.ValueType] = None,
    ):
        """
        Create metadata for a derived signal.

        Args:
            unit:                   Unit of the signal.
            decimals:               Number of decimals to use when displaying signal values.
            signal_type:            Type of the signal.
            downsampling_method:    The default downsampling method to use when resampling.
            change:                 The method used to calculate changes in this signal.
        """
        self.unit = unit
        self.decimals = decimals
        self.signal_type = signal_type
        self.downsampling_method = downsampling_method
        self.change = change

    @staticmethod
    def from_proto(metadata: ProtoDerivedSignalMetadata) -> "DerivedSignalMetaData":
        """Create a DerivedSignalMetaData from the given protobuf DerivedSignalMetaData."""
        return DerivedSignalMetaData(
            unit=DerivedSignalUnit(metadata.unit),
            decimals=metadata.decimals.value if metadata.HasField("decimals") else None,
            signal_type=DerivedSignalType(metadata.type),
            downsampling_method=(
                Aggregation.ValueType(metadata.downsampling_method)
                if metadata.downsampling_method
                else None
            ),
            change=Change.ValueType(metadata.change) if metadata.change else None,
        )

    def to_proto(self) -> ProtoDerivedSignalMetadata:
        """Create a protobuf DerivedSignalMetadata from this DerivedSignalMetadata."""
        return ProtoDerivedSignalMetadata(
            unit=self.unit.value,
            decimals=Int32Value(value=self.decimals) if self.decimals is not None else None,
            type=self.signal_type.value,
            downsampling_method=(
                int(self.downsampling_method)
                if self.downsampling_method
                else 0  # type: ignore[arg-type]
            ),
            change=int(self.change) if self.change else 0,  # type: ignore[arg-type]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DerivedSignalMetaData):
            return False
        return (
            self.decimals == other.decimals
            and self.unit == other.unit
            and self.signal_type == other.signal_type
            and self.downsampling_method == other.downsampling_method
            and self.change == other.change
        )

    def __repr__(self) -> str:
        return (
            f"DerivedSignalMetaData(decimals='{self.decimals}', unit='{self.unit}', signal_type="
            f"'{self.signal_type}', downsampling_method='{self.downsampling_method}', "
            f"change='{self.change}')"
        )


class DerivedSignal:
    """
    A derived signal in the Analytics API.

    Attributes:
        name:           The resource name of the derived signal, for example "derivedSignals/123".
                        The resource name is not namespaced, and the identifier is always an
                        integer. It is required in all operations except the create operation.
        label:          The label of the derived signal.
        expression:     The expression of the derived signal.
        description:    A description of the derived signal.
        display_name:   The display name of the signal.
        metadata:       Metadata of the derived signal.
    """

    def __init__(
        self,
        name: Optional[str],
        label: str,
        expression: str,
        description: Optional[str] = None,
        display_name: Optional[str] = None,
        metadata: DerivedSignalMetaData = DerivedSignalMetaData(),
    ):
        """
        Create a derived signal in the Analytics API.

        Args:
            name:           The resource name of the derived signal, for example
                            "derivedSignals/123". The resource name is not namespaced,
                            and the identifier is always an integer. It is required in all
                            operations except the create operation.
            label:          The label of the derived signal.
            expression:     The expression of the derived signal.
            description:    A description of the derived signal.
            display_name:   The display name of the signal.
            metadata:       Metadata of the derived signal.
        """
        self.name = name
        self.label = label
        self.expression = expression
        self.description = description
        self.display_name = display_name
        self.metadata = metadata

    @staticmethod
    def from_analytics_api_proto(signal: ProtoDerivedSignal) -> "DerivedSignal":
        """Create a DerivedSignal from the given Analytics API protobuf DerivedSignal."""
        return DerivedSignal(
            name=signal.name,
            label=signal.label,
            expression=signal.expression,
            description=signal.description if signal.description else None,
            display_name=signal.display_name if signal.display_name else None,
            metadata=DerivedSignalMetaData.from_proto(signal.metadata),
        )

    @staticmethod
    def from_data_api_proto(
        data_api_signal: ProtoDataApiDerivedSignal,
    ) -> "DerivedSignal":
        """
        Create a DerivedSignal from the given Data API protobuf DerivedSignal.

        Maps the compatible fields (name, label, expression, description, display_name,
        downsampling_method, change). Drops Data API specific fields data_sets,
        highlighted and entity_set.
        """
        metadata = DerivedSignalMetaData(
            downsampling_method=(
                Aggregation.ValueType(data_api_signal.downsampling_method)
                if data_api_signal.downsampling_method
                else None
            ),
            change=Change.ValueType(data_api_signal.change) if data_api_signal.change else None,
        )

        return DerivedSignal(
            name=data_api_signal.name,
            label=data_api_signal.label,
            expression=data_api_signal.expression,
            description=data_api_signal.description if data_api_signal.description else None,
            display_name=data_api_signal.display_name if data_api_signal.display_name else None,
            metadata=metadata,
        )

    def to_analytics_api_proto(self) -> ProtoDerivedSignal:
        """Create an Analytics API protobuf DerivedSignal from this DerivedSignal."""
        return ProtoDerivedSignal(
            name=self.name,
            label=self.label,
            expression=self.expression,
            description=self.description,
            display_name=self.display_name,
            metadata=self.metadata.to_proto(),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DerivedSignal):
            return False
        return (
            self.name == other.name
            and self.label == other.label
            and self.expression == other.expression
            and self.description == other.description
            and self.display_name == other.display_name
            and self.metadata == other.metadata
        )

    def __repr__(self) -> str:
        return (
            f"DerivedSignal(name='{self.name}', label='{self.label}', "
            f"expression='{self.expression}', description='{self.description}', "
            f"display_name='{self.display_name}', metadata={self.metadata})"
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, DerivedSignal):
            raise ValueError(f"Cannot compare DerivedSignal to non-DerivedSignal: {other}")
        if self.name is None or other.name is None:
            raise ValueError("Cannot compare DerivedSignals without name.")
        return self.name < other.name
