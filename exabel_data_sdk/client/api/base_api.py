import grpc

from exabel_data_sdk.client.client_config import ClientConfig


class BaseApi:
    """
    Base class for API classes.
    """

    def __init__(self, config: ClientConfig):
        self.config = config
        self.metadata = [("x-client-name", config.client_name)]
        if config.api_key == "NO_KEY":
            # Use an insecure channel. This can be used for local testing.
            self.channel = grpc.insecure_channel(config.host + ":" + str(config.port))
        else:
            assert config.api_key is not None
            self.metadata.append(("x-api-key", config.api_key))
            self.channel = grpc.secure_channel(
                config.host + ":" + str(config.port), grpc.ssl_channel_credentials()
            )
