from enum import Enum

from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiSource as ProtoKpiSource,
)


class KpiSource(Enum):
    """Enum representing the source of a KPI."""

    # Visible Alpha.
    VISIBLE_ALPHA = 1

    # Factset.
    FACTSET = 2

    def to_proto(self) -> ProtoKpiSource.ValueType:
        """Create a protobuf KpiSource from this KpiSource."""
        return (
            ProtoKpiSource.KPI_SOURCE_FACTSET
            if self == KpiSource.FACTSET
            else ProtoKpiSource.KPI_SOURCE_VISIBLE_ALPHA
        )
