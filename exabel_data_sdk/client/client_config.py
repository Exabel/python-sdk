import os
from typing import Optional, Sequence, Tuple


class DefaultConfig:
    """
    Default configuration.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("EXABEL_API_KEY")
        self.client_name = os.getenv("EXABEL_CLIENT_NAME", "Exabel Python SDK")
        self.data_api_host = os.getenv("EXABEL_DATA_API_HOST", "data.api.exabel.com")
        self.analytics_api_host = os.getenv("EXABEL_ANALYTICS_API_HOST", "analytics.api.exabel.com")
        self.management_api_host = os.getenv(
            "EXABEL_MANAGEMENT_API_HOST", "management.api.exabel.com"
        )
        self.data_api_port = int(os.getenv("EXABEL_DATA_API_PORT", "21443"))
        self.analytics_api_port = int(os.getenv("EXABEL_ANALYTICS_API_PORT", "21443"))
        self.management_api_port = int(os.getenv("EXABEL_MANAGEMENT_API_PORT", "21443"))
        self.timeout = int(os.getenv("EXABEL_TIMEOUT", "60"))
        self.root_certificates: Optional[str] = None
        self.extra_headers: Sequence[Tuple[str, str]] = ()


class ClientConfig(DefaultConfig):
    """
    Exabel SDK configuration.
    """

    def __init__(
        self,
        api_key: str = None,
        client_name: str = None,
        data_api_host: str = None,
        analytics_api_host: str = None,
        management_api_host: str = None,
        data_api_port: int = None,
        analytics_api_port: int = None,
        management_api_port: int = None,
        timeout: int = None,
        root_certificates: str = None,
        extra_headers: Sequence[Tuple[str, str]] = None,
    ):
        """
        Initialize a new client configuration.

        Args:
            api_key:             API key to use.
            client_name:         Name of this client.
            data_api_host:       Exabel Data API host.
            analytics_api_host:  Exabel Analytics API host.
            management_api_host: Exabel Management API host.
            data_api_port:       Exabel Data API port.
            analytics_api_port:  Exabel Analytics API port.
            management_api_port: Exabel Management API port.
            timeout:             Default timeout in seconds to use for API requests.
            root_certificates:   Additional allowed root certificates for verifying TLS connection.
            extra_headers:       A list of headers to include in the request.
        """
        super().__init__()

        self.api_key = api_key or self.api_key
        self.client_name = client_name or self.client_name
        self.data_api_host = data_api_host or self.data_api_host
        self.analytics_api_host = analytics_api_host or self.analytics_api_host
        self.management_api_host = management_api_host or self.management_api_host
        self.data_api_port = data_api_port or self.data_api_port
        self.analytics_api_port = analytics_api_port or self.analytics_api_port
        self.management_api_port = management_api_port or self.management_api_port
        self.timeout = timeout or self.timeout
        self.root_certificates = root_certificates or self.root_certificates
        self.extra_headers = extra_headers or self.extra_headers

        if not self.api_key:
            raise ValueError("No API key given. Use of the Exabel SDK requires an API key.")
