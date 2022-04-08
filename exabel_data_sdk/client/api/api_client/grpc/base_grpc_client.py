import grpc

from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.client_config import ClientConfig


class BaseGrpcClient:
    """
    Base class for clients that access the Exabel API with gRPC.
    """

    def __init__(self, config: ClientConfig, api_group: ExabelApiGroup):
        self.config = config
        self.metadata = [("x-client-name", config.client_name)]
        host = api_group.get_host(config)
        port = api_group.get_port(config)
        if config.api_key == "NO_KEY":
            # Use an insecure channel. This can be used for local testing.
            self.channel = grpc.insecure_channel(host + ":" + str(port))
        else:
            assert config.api_key is not None
            self.metadata.append(("x-api-key", config.api_key))
            self.channel = grpc.secure_channel(
                host + ":" + str(port),
                grpc.ssl_channel_credentials(root_certificates=config.root_certificates),
            )
        for header in self.config.extra_headers:
            self.metadata.append(header)
