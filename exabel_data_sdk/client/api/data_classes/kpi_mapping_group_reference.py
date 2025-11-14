from dataclasses import dataclass

from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiMappingGroupReference as ProtoKpiMappingGroupReference,
)


@dataclass
class KpiMappingGroupReference:
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
    def from_proto(proto: ProtoKpiMappingGroupReference) -> "KpiMappingGroupReference":
        """Create a KpiMappingGroupReference from the given protobuf KpiMappingGroupReference."""
        return KpiMappingGroupReference(
            name=proto.name,
            display_name=proto.display_name,
            vendor_display_name=proto.vendor_display_name,
        )
