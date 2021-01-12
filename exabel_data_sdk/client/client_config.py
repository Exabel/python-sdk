import os


class DefaultConfig:
    """
    Default configuration.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("EXABEL_API_KEY")
        self.client_name = os.getenv("EXABEL_CLIENT_NAME", "Exabel Python SDK")
        self.host = os.getenv("EXABEL_HOST", "data.api.exabel.com")
        self.port = int(os.getenv("EXABEL_PORT", "21443"))
        self.timeout = int(os.getenv("EXABEL_TIMEOUT", "30"))


class ClientConfig(DefaultConfig):
    """
    Exabel SDK configuration.
    """

    def __init__(
        self,
        api_key: str = None,
        client_name: str = None,
        host: str = None,
        port: int = None,
        timeout: int = None,
    ):
        """
        Initialize a new client configuration.

        Args:
            api_key:        API key to use.
            client_name:    Name of this client.
            host:           Exabel API host.
            port:           Exabel API port.
            timeout:        Default timeout in seconds to use for API requests.
        """
        super().__init__()

        self.api_key = api_key or self.api_key
        self.client_name = client_name or self.client_name
        self.host = host or self.host
        self.port = port or self.port
        self.timeout = timeout or self.timeout

        if not self.api_key:
            raise ValueError("No API key given. Use of the Exabel SDK requires an API key.")
