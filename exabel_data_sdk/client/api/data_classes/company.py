from dataclasses import dataclass

from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import Company as ProtoCompany


@dataclass
class Company:
    """
    A company.

    Attributes:
        name:               The resource name of the company.
        display_name:       The display name of the company.
        bloomberg_ticker:   The Bloomberg ticker of the company.
    """

    name: str
    display_name: str
    bloomberg_ticker: str

    @staticmethod
    def from_proto(proto: ProtoCompany) -> "Company":
        """Create a Company from the given protobuf Company."""
        return Company(
            name=proto.name,
            display_name=proto.display_name,
            bloomberg_ticker=proto.bloomberg_ticker,
        )
