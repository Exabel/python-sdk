import json

import grpc

from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.client_config import ClientConfig

SIXTEEN_MEGABYTES_IN_BYTES = 16 * 1024 * 1024

# Retry parameters
DEFAULT_MAX_ATTEMPTS = 5
DEFAULT_INITIAL_BACKOFF_SECONDS = 0.1
DEFAULT_MAX_BACKOFF_SECONDS = 5
DEFAULT_BACKOFF_MULTIPLIER = 2


class BaseGrpcClient:
    """
    Base class for clients that access the Exabel API with gRPC.
    """

    def __init__(self, config: ClientConfig, api_group: ExabelApiGroup):
        self.config = config
        self.metadata = [("x-client-name", config.client_name)]
        common_kwargs = {
            "target": f"{api_group.get_host(config)}:{api_group.get_port(config)}",
            # When importing time series, we may receive a large amount of precondition failure
            # violations in the trailing metadata, therefore we increase the maximum metadata size.
            "options": (
                ("grpc.max_metadata_size", SIXTEEN_MEGABYTES_IN_BYTES),
                ("grpc.service_config", self._get_service_config()),
            ),
        }
        if config.api_key == "NO_KEY":
            # Use an insecure channel. This can be used for local testing.
            self.channel = grpc.insecure_channel(**common_kwargs)
        else:
            assert config.api_key is not None
            self.metadata.append(("x-api-key", config.api_key))
            self.channel = grpc.secure_channel(
                credentials=grpc.ssl_channel_credentials(
                    root_certificates=config.root_certificates
                ),
                **common_kwargs,
            )
        for header in self.config.extra_headers:
            self.metadata.append(header)

    def _get_service_config(
        self,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        initial_backoff: float = DEFAULT_INITIAL_BACKOFF_SECONDS,
        max_backoff: float = DEFAULT_MAX_BACKOFF_SECONDS,
        backoff_multiplier: int = DEFAULT_BACKOFF_MULTIPLIER,
    ) -> str:
        """
        Returns a JSON string to use for grpc.service_config option when creating a grpc channel
        """
        return json.dumps(
            {
                "methodConfig": [
                    {
                        "name": [{}],
                        "retryPolicy": {
                            "maxAttempts": max_attempts,
                            "initialBackoff": f"{initial_backoff}s",
                            "maxBackoff": f"{max_backoff}s",
                            "backoffMultiplier": backoff_multiplier,
                            "retryableStatusCodes": [
                                "CANCELLED",
                                "UNKNOWN",
                                "DEADLINE_EXCEEDED",
                                "RESOURCE_EXHAUSTED",
                                "ABORTED",
                                "INTERNAL",
                                "UNAVAILABLE",
                            ],
                        },
                    }
                ]
            }
        )
