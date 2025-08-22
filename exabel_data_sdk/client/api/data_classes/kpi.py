from dataclasses import dataclass
from enum import Enum
from typing import Optional

from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import Kpi as ProtoKpi


class KpiType(Enum):
    """Enum representing the KPI type."""

    # Visible Alpha.
    VISIBLE_ALPHA = "VISIBLE_ALPHA_STANDARD_KPI"
    # FactSet Estimates.
    FACTSET_ESTIMATES = "FACTSET_ESTIMATES"
    # FactSet Fundamentals.
    FACTSET_FUNDAMENTALS = "FACTSET_FUNDAMENTALS"
    # FactSet Segments.
    FACTSET_SEGMENTS = "FACTSET_SEGMENTS"


@dataclass
class Kpi:
    """
    A KPI.

    Attributes:
        type:           The type of the KPI.
        value:          The value of the KPI.
        freq:           The frequency of the KPI.
        display_name:   The display name of the KPI.
        is_ratio:       Whether the KPI is a ratio.
    """

    type: KpiType
    value: str
    freq: str
    display_name: Optional[str] = None
    is_ratio: Optional[bool] = None

    @staticmethod
    def from_proto(proto: ProtoKpi) -> "Kpi":
        """Create a KPI from the given protobuf KPI."""
        return Kpi(
            type=KpiType(proto.type),
            value=proto.value,
            freq=proto.freq,
            display_name=proto.display_name,
            is_ratio=proto.is_ratio if proto.HasField("is_ratio") else None,
        )

    def to_proto(self) -> ProtoKpi:
        """
        Create a proto KPI from this KPI.

        Only the type, value, and freq fields are set.
        """
        return ProtoKpi(
            type=self.type.value,
            value=self.value,
            freq=self.freq,
        )
