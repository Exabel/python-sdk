from typing import Sequence

from exabel.client.api.calendar_api import CalendarApi
from exabel.client.api.data_set_api import DataSetApi
from exabel.client.api.derived_signal_api import DerivedSignalApi
from exabel.client.api.entity_api import EntityApi
from exabel.client.api.export_api import ExportApi
from exabel.client.api.holiday_api import HolidayApi
from exabel.client.api.kpi_api import KpiApi
from exabel.client.api.library_api import LibraryApi
from exabel.client.api.namespace_api import NamespaceApi
from exabel.client.api.prediction_model_api import PredictionModelApi
from exabel.client.api.relationship_api import RelationshipApi
from exabel.client.api.signal_api import SignalApi
from exabel.client.api.tag_api import TagApi
from exabel.client.api.time_series_api import TimeSeriesApi
from exabel.client.api.user_api import UserApi
from exabel.client.client_config import ClientConfig


class ExabelClient:
    """
    SDK entry point.
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
        Initialize a new client.

        Args:
            api_key:             API key to use. Only one of api_key and access_token must be
                                 given. If set to the value 'NO_KEY', the client will use an
                                 insecure channel, typically used for local testing.
            access_token:        Access token to use. Only one of api_key and access_token must be
                                 given.
            client_name:         Override name of this client. Default name is "Exabel Python SDK".
            data_api_host:       Override default Exabel Data API host.
            analytics_api_host:  Override default Exabel Analytics API host.
            management_api_host: Override default Exabel Management API host.
            export_api_host:     Override default Exabel Export API host.
            data_api_port:       Override default Exabel Data API port.
            analytics_api_port:  Override default Exabel Analytics API port.
            management_api_port: Override default Exabel Management API port.
            export_api_port:     Override default Exabel Export API port.
            timeout:             Override default timeout in seconds to use for API requests (only
                                 affects gRPC APIs).
            retries:             Override default number of retries for requests (only affects Export
                                 API).
            root_certificates:   Additional allowed root certificates for verifying TLS connection
                                 (only affects gRPC APIs).
        """
        config = ClientConfig(
            api_key=api_key,
            access_token=access_token,
            client_name=client_name,
            data_api_host=data_api_host,
            analytics_api_host=analytics_api_host,
            management_api_host=management_api_host,
            export_api_host=export_api_host,
            data_api_port=data_api_port,
            analytics_api_port=analytics_api_port,
            management_api_port=management_api_port,
            export_api_port=export_api_port,
            timeout=timeout,
            retries=retries,
            root_certificates=root_certificates,
            extra_headers=extra_headers,
        )

        self.entity_api = EntityApi(config)
        self.signal_api = SignalApi(config)
        self.time_series_api = TimeSeriesApi(config)
        self.relationship_api = RelationshipApi(config)
        self.data_set_api = DataSetApi(config)
        self.prediction_model_api = PredictionModelApi(config)
        self.derived_signal_api = DerivedSignalApi(config)
        self.tag_api = TagApi(config)
        self.user_api = UserApi(config)
        self.library_api = LibraryApi(config)
        self.kpi_api = KpiApi(config)
        self.calendar_api = CalendarApi(config)
        self.holiday_api = HolidayApi(config)
        self.namespace_api = NamespaceApi(config)
        self.export_api = ExportApi(config)
        self._namespace: str | None = None

    @property
    def namespace(self) -> str:
        """The (writeable) namespace of the current customer."""
        if self._namespace is None:
            self._namespace = self.namespace_api.get_writeable_namespace().name.split("/")[-1]
        return self._namespace
