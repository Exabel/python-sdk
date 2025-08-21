from dataclasses import dataclass

from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiMappingGroup as ProtoKpiMappingGroup,
)


@dataclass
class KpiMappingGroup:
    """
    A KPI mapping group.

    Attributes:
        name:                   The resource name of the KPI mapping group.
        display_name:           The display name of the KPI mapping group.
        vendor_display_name:    The display name of the vendor the group belongs to.
    """

    name: str
    display_name: str
    vendor_display_name: str

    @staticmethod
    def from_proto(proto: ProtoKpiMappingGroup) -> "KpiMappingGroup":
        """Create a KpiMappingGroup from the given protobuf KpiMappingGroup."""
        return KpiMappingGroup(
            name=proto.name,
            display_name=proto.display_name,
            vendor_display_name=proto.vendor_display_name,
        )
