from enum import Enum, auto

from exabel_data_sdk.client.client_config import ClientConfig


class ExabelApiGroup(Enum):
    """
    Exabel API groups.
    """

    # Data API.
    DATA_API = auto()

    # Analytics API.
    ANALYTICS_API = auto()

    # Management API.
    MANAGEMENT_API = auto()

    def get_host(self, config: ClientConfig) -> str:
        """Return the API host for this API group."""
        if self == ExabelApiGroup.DATA_API:
            return config.data_api_host
        if self == ExabelApiGroup.ANALYTICS_API:
            return config.analytics_api_host
        if self == ExabelApiGroup.MANAGEMENT_API:
            return config.management_api_host
        raise ValueError(f"Unknown ExabelApiGroup: {self.name}")

    def get_port(self, config: ClientConfig) -> int:
        """Return the API port for this API group."""
        if self == ExabelApiGroup.DATA_API:
            return config.data_api_port
        if self == ExabelApiGroup.ANALYTICS_API:
            return config.analytics_api_port
        if self == ExabelApiGroup.MANAGEMENT_API:
            return config.management_api_port
        raise ValueError(f"Unknown ExabelApiGroup: {self.name}")
