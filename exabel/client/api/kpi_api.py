import logging
from typing import Literal, Sequence

import pandas as pd

from exabel.client.api.api_client.grpc.kpi_grpc_client import KpiGrpcClient
from exabel.client.api.data_classes.company_kpi_mapping_results import (
    CompanyKpiMappingResults,
)
from exabel.client.api.data_classes.company_kpi_models import CompanyKpiModels
from exabel.client.api.data_classes.kpi import Kpi, KpiType
from exabel.client.api.data_classes.kpi_mapping_result_data import KpiMappingResultData
from exabel.client.api.data_classes.kpi_screen_results import KpiScreenCompanyResult
from exabel.client.api.data_classes.kpi_source import KpiSource
from exabel.client.api.data_classes.model_results import (
    BaseModelResults,
    HierarchicalModelResults,
)
from exabel.client.api.data_classes.paging_result import PagingResult
from exabel.client.client_config import ClientConfig
from exabel.stubs.exabel.api.analytics.v1.all_pb2 import (
    FiscalPeriodSelector,
    RelativeFiscalPeriodSelector,
)
from exabel.stubs.exabel.api.analytics.v1.kpi_service_pb2 import (
    ListCompanyBaseModelResultsRequest,
    ListCompanyHierarchicalModelResultsRequest,
    ListCompanyKpiMappingResultsRequest,
    ListCompanyKpiModelResultsRequest,
    ListKpiMappingResultsRequest,
    ListKpiScreenResultsRequest,
)
from exabel.stubs.exabel.api.time.date_pb2 import Date

logger = logging.getLogger(__name__)


class KpiApi:
    """
    API class for KPI operations.
    """

    def __init__(self, config: ClientConfig):
        self.client = KpiGrpcClient(config)

    def list_kpi_mapping_results(
        self, kpi_mapping: str, page_size: int = 20, page_token: str = ""
    ) -> PagingResult[CompanyKpiMappingResults]:
        """
        List KPI mapping results for a single KPI mapping collection.

        Args:
            kpi_mapping:    KPI mapping resource name.
            page_size:      The maximum number of results to return.
            page_token:     The page token to resume the results from.
        """
        request = ListKpiMappingResultsRequest(
            parent=kpi_mapping, page_size=page_size, page_token=page_token
        )
        response = self.client.list_kpi_mapping_results(request)
        return PagingResult(
            [CompanyKpiMappingResults.from_proto(result) for result in response.results],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    def list_company_base_model_results(
        self,
        company: str,
        source_filter: KpiSource | None = None,
        fiscal_period: Literal["previous", "current", "next"] | pd.Timestamp = "current",
        freq: Literal["FQ", "FS", "FY"] | None = None,
    ) -> BaseModelResults:
        """
        List base model results for a company.

        Args:
            company:        Company resource name.
            source_filter:  DEPRECATED. KPI source filtering is now determined by user settings.
                            This parameter is ignored. Set user preferences via UserApi instead.
            fiscal_period:  Fiscal period to retrieve data for.
            freq:           Frequency to retrieve data for. If not provided, frequency is
                            determined based on KPI counts.
        """
        if source_filter is not None:
            logger.warning(
                "source_filter parameter is deprecated and ignored. "
                "KPI source filtering is now determined by user settings. ",
            )
        request = ListCompanyBaseModelResultsRequest(
            parent=company,
            period=self._get_fiscal_period_selector(fiscal_period, freq),
        )
        response = self.client.list_company_base_model_results(request)
        return BaseModelResults.from_proto(response)

    def list_company_hierarchical_model_results(
        self,
        company: str,
        source_filter: KpiSource | None = None,
        fiscal_period: Literal["previous", "current", "next"] | pd.Timestamp = "current",
        freq: Literal["FQ", "FS", "FY"] | None = None,
    ) -> HierarchicalModelResults:
        """
        List hierarchical model results for a company.

        Args:
            company:        Company resource name.
            source_filter:  DEPRECATED. KPI source filtering is now determined by user settings.
                            This parameter is ignored. Set user preferences via UserApi instead.
            fiscal_period:  Fiscal period to retrieve data for.
            freq:           Frequency to retrieve data for. If not provided, frequency is
                            determined based on KPI counts.
        """
        if source_filter is not None:
            logger.warning(
                "source_filter parameter is deprecated and ignored. "
                "KPI source filtering is now determined by user settings. ",
            )
        request = ListCompanyHierarchicalModelResultsRequest(
            parent=company,
            period=self._get_fiscal_period_selector(fiscal_period, freq),
        )
        response = self.client.list_company_hierarchical_model_results(request)
        return HierarchicalModelResults.from_proto(response)

    def list_company_kpi_mapping_results(
        self,
        company: str,
        kpi_type: KpiType,
        kpi_value: str,
        kpi_freq: Literal["FQ", "FS", "FY"],
    ) -> Sequence[KpiMappingResultData]:
        """
        List KPI mapping results for a single company KPI.

        Args:
            company:    Company resource name.
            kpi_type:   KPI type.
            kpi_value:  KPI value.
            kpi_freq:   KPI frequency.
        """
        request = ListCompanyKpiMappingResultsRequest(
            parent=company, kpi=Kpi(type=kpi_type, value=kpi_value, freq=kpi_freq).to_proto()
        )
        response = self.client.list_company_kpi_mapping_results(request)
        return [KpiMappingResultData.from_proto(result) for result in response.results]

    def list_company_kpi_model_results(
        self, company: str, kpi_type: KpiType, kpi_value: str, kpi_freq: Literal["FQ", "FS", "FY"]
    ) -> CompanyKpiModels:
        """
        List model results for a single company KPI.

        Args:
            company:    Company resource name.
            kpi_type:   KPI type.
            kpi_value:  KPI value.
            kpi_freq:   KPI frequency.
        """
        request = ListCompanyKpiModelResultsRequest(
            parent=company, kpi=Kpi(type=kpi_type, value=kpi_value, freq=kpi_freq).to_proto()
        )
        response = self.client.list_company_kpi_model_results(request)
        return CompanyKpiModels.from_proto(response)

    def list_kpi_screen_results(
        self, kpi_screen: str, page_size: int = 20, page_token: str = ""
    ) -> PagingResult[KpiScreenCompanyResult]:
        """
        List KPI screen results.

        Args:
            kpi_screen:    KPI screen resource name.
            page_size:     The maximum number of results to return.
            page_token:    The page token to resume the results from.
        """
        request = ListKpiScreenResultsRequest(
            name=kpi_screen, page_size=page_size, page_token=page_token
        )
        response = self.client.list_kpi_screen_results(request)
        return PagingResult(
            [KpiScreenCompanyResult.from_proto(result) for result in response.results],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    @staticmethod
    def _get_fiscal_period_selector(
        fiscal_period: Literal["previous", "current", "next"] | pd.Timestamp,
        freq: Literal["FQ", "FS", "FY"] | None,
    ) -> FiscalPeriodSelector:
        if freq not in ["FQ", "FS", "FY", None]:
            raise ValueError("Frequency must be one of FQ, FS and FY.")

        if fiscal_period == "previous":
            return FiscalPeriodSelector(
                relative_selector=RelativeFiscalPeriodSelector.PREVIOUS, freq=freq
            )
        if fiscal_period == "current":
            return FiscalPeriodSelector(
                relative_selector=RelativeFiscalPeriodSelector.CURRENT, freq=freq
            )
        if fiscal_period == "next":
            return FiscalPeriodSelector(
                relative_selector=RelativeFiscalPeriodSelector.NEXT, freq=freq
            )
        if isinstance(fiscal_period, pd.Timestamp):
            return FiscalPeriodSelector(
                period_end=Date(
                    year=fiscal_period.year, month=fiscal_period.month, day=fiscal_period.day
                ),
                freq=freq,
            )
        raise ValueError(f"Invalid fiscal period: {fiscal_period}")
