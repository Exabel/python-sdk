from typing import Sequence, Tuple

from exabel_data_sdk.client.api.data_set_api import DataSetApi
from exabel_data_sdk.client.api.derived_signal_api import DerivedSignalApi
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.api.library_api import LibraryApi
from exabel_data_sdk.client.api.namespace_api import NamespaceApi
from exabel_data_sdk.client.api.prediction_model_api import PredictionModelApi
from exabel_data_sdk.client.api.relationship_api import RelationshipApi
from exabel_data_sdk.client.api.signal_api import SignalApi
from exabel_data_sdk.client.api.time_series_api import TimeSeriesApi
from exabel_data_sdk.client.api.user_api import UserApi
from exabel_data_sdk.client.client_config import ClientConfig


class ExabelClient:
    """
    SDK entry point.
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
        use_json: bool = False,
        extra_headers: Sequence[Tuple[str, str]] = None,
    ):
        """
        Initialize a new client.

        Args:
            api_key:             API key to use. If not set, the API key must be set using the
                                 environment variable EXABEL_API_KEY. If set to the value 'NO_KEY',
                                 the client will use an insecure channel, typically used for local
                                 testing.
            client_name:         Override name of this client. Default name is "Exabel Python SDK".
            data_api_host:       Override default Exabel Data API host.
            analytics_api_host:  Override default Exabel Analytics API host.
            management_api_host: Override default Exabel Management API host.
            data_api_port:       Override default Exabel Data API port.
            analytics_api_port:  Override default Exabel Analytics API port.
            management_api_port: Override default Exabel Management API port.
            timeout:             Override default timeout in seconds to use for API requests.
            root_certificates:   Additional allowed root certificates for verifying TLS connection.
            use_json:            Whether requests should be sent as JSON over HTTP rather than gRPC.
        """
        config = ClientConfig(
            api_key=api_key,
            client_name=client_name,
            data_api_host=data_api_host,
            analytics_api_host=analytics_api_host,
            management_api_host=management_api_host,
            data_api_port=data_api_port,
            analytics_api_port=analytics_api_port,
            management_api_port=management_api_port,
            timeout=timeout,
            root_certificates=root_certificates,
            extra_headers=extra_headers,
        )

        self.entity_api = EntityApi(config, use_json)
        self.signal_api = SignalApi(config, use_json)
        self.time_series_api = TimeSeriesApi(config, use_json)
        self.relationship_api = RelationshipApi(config, use_json)
        self.data_set_api = DataSetApi(config, use_json)
        self.prediction_model_api = PredictionModelApi(config, use_json)
        self.derived_signal_api = DerivedSignalApi(config, use_json)
        self.user_api = UserApi(config, use_json)
        self.library_api = LibraryApi(config, use_json)
        self.namespace_api = NamespaceApi(config, use_json)
