import os
from typing import Sequence

FIFTEEN_MINUTES_IN_SECONDS = 15 * 60


class DefaultConfig:
    """
    Default configuration.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("EXABEL_API_KEY")
        self.access_token = os.getenv("EXABEL_ACCESS_TOKEN")
        self.client_name = os.getenv("EXABEL_CLIENT_NAME", "Exabel Python SDK")
        self.data_api_host = os.getenv("EXABEL_DATA_API_HOST", "data.api.exabel.com")
        self.analytics_api_host = os.getenv("EXABEL_ANALYTICS_API_HOST", "analytics.api.exabel.com")
        self.management_api_host = os.getenv(
            "EXABEL_MANAGEMENT_API_HOST", "management.api.exabel.com"
        )
        self.export_api_host = os.getenv("EXABEL_EXPORT_API_HOST", "export.api.exabel.com")
        self.data_api_port = int(os.getenv("EXABEL_DATA_API_PORT", "21443"))
        self.analytics_api_port = int(os.getenv("EXABEL_ANALYTICS_API_PORT", "21443"))
        self.management_api_port = int(os.getenv("EXABEL_MANAGEMENT_API_PORT", "21443"))
        self.export_api_port = int(os.getenv("EXABEL_EXPORT_API_PORT", "443"))
        self.timeout = int(os.environ.get("EXABEL_TIMEOUT", FIFTEEN_MINUTES_IN_SECONDS))
        self.retries = int(os.getenv("EXABEL_RETRIES", "0"))
        self.root_certificates: str | None = None
        self.extra_headers: Sequence[tuple[str, str]] = ()


class ClientConfig(DefaultConfig):
    """
    Exabel SDK configuration.
    """

    def __init__(
        self,
        api_key: str | None = None,
        access_token: str | None = None,
        client_name: str | None = None,
        data_api_host: str | None = None,
        analytics_api_host: str | None = None,
        management_api_host: str | None = None,
        export_api_host: str | None = None,
        data_api_port: int | None = None,
        analytics_api_port: int | None = None,
        management_api_port: int | None = None,
        export_api_port: int | None = None,
        timeout: int | None = None,
        retries: int | None = None,
        root_certificates: str | None = None,
        extra_headers: Sequence[tuple[str, str]] | None = None,
    ):
        """
        Initialize a new client configuration.

        Args:
            api_key:             API key to use.
            access_token:        Access token to use.
            client_name:         Name of this client.
            data_api_host:       Exabel Data API host.
            analytics_api_host:  Exabel Analytics API host.
            management_api_host: Exabel Management API host.
            export_api_host:     Exabel Export API host.
            data_api_port:       Exabel Data API port.
            analytics_api_port:  Exabel Analytics API port.
            management_api_port: Exabel Management API port.
            export_api_port:     Exabel Export API port.
            timeout:             Default timeout in seconds to use for API requests.
            retries:             Default number of retries to use for API requests.
            root_certificates:   Additional allowed root certificates for verifying TLS connection.
            extra_headers:       A list of headers to include in the request.
        """
        super().__init__()

        # Arguments take precedence over environment variables
        if api_key or access_token:
            self.api_key = api_key
            self.access_token = access_token
        self.client_name = client_name or self.client_name
        self.data_api_host = data_api_host or self.data_api_host
        self.analytics_api_host = analytics_api_host or self.analytics_api_host
        self.management_api_host = management_api_host or self.management_api_host
        self.export_api_host = export_api_host or self.export_api_host
        self.data_api_port = data_api_port or self.data_api_port
        self.analytics_api_port = analytics_api_port or self.analytics_api_port
        self.management_api_port = management_api_port or self.management_api_port
        self.export_api_port = export_api_port or self.export_api_port
        self.timeout = timeout or self.timeout
        self.retries = retries or self.retries
        self.root_certificates = root_certificates or self.root_certificates
        self.extra_headers = extra_headers or self.extra_headers

        if self.api_key and self.access_token:
            raise ValueError(
                "Both API key and access token given. Only one of these should be set."
            )

        if not self.api_key and not self.access_token:
            raise ValueError(
                "No API key or access token given. Use of the Exabel SDK requires either an "
                "API key or access token."
            )
