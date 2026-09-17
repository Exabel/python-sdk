from abc import ABC, abstractmethod

from exabel.stubs.exabel.api.management.v1.all_pb2 import (
    ListTableColumnsRequest,
    ListTableColumnsResponse,
    ListWidgetsRequest,
    ListWidgetsResponse,
)


class DashboardApiClient(ABC):
    """
    Superclass for clients that send dashboard requests to the Exabel Management API.
    """

    @abstractmethod
    def list_widgets(self, request: ListWidgetsRequest) -> ListWidgetsResponse:
        """List the widgets in a dashboard."""

    @abstractmethod
    def list_table_columns(self, request: ListTableColumnsRequest) -> ListTableColumnsResponse:
        """List the columns of one dashboard table widget."""
