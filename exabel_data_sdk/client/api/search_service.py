import itertools
from typing import Mapping, Sequence, Tuple, TypeVar, Union

from exabel_data_sdk.client.api.api_client.entity_api_client import EntityApiClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    SearchEntitiesRequest,
    SearchEntitiesResponse,
    SearchTerm,
)

_COMPANY_ENTITY_TYPE = "entityTypes/company"
_SECURITY_ENTITY_TYPE = "entityTypes/security"
_LISTING_ENTITY_TYPE = "entityTypes/listing"

TKey = TypeVar("TKey")


class SearchService:
    """
    Service for entity search.
    """

    def __init__(self, client: EntityApiClient):
        self.client = client

    def company_by_isin(self, *isins: str) -> Mapping[str, Entity]:
        """
        Look up companies by ISIN (International Securities Identification Number).

        The return value is a dict with the input values as keys and with the corresponding Entity
        objects as values. ISINs which did not return any results, are not included.
        """
        return self._company_by_field("isin", *isins)

    def security_by_isin(self, *isins: str) -> Mapping[str, Entity]:
        """
        Look up securities by ISIN (International Securities Identification Number).

        The return value is a dict with the input values as keys and with the corresponding Entity
        objects as values. ISINs which did not return any results, are not included.
        """
        return self._security_by_field("isin", *isins)

    def company_by_bloomberg_ticker(self, *tickers: str) -> Mapping[str, Entity]:
        """
        Look up companies by Bloomberg tickers.

        The return value is a dict with the input values as keys and with the corresponding Entity
        objects as values. Tickers which did not return any results, are not included.
        """
        return self._company_by_field("bloomberg_ticker", *tickers)

    def company_by_bloomberg_symbol(self, *symbols: str) -> Mapping[str, Entity]:
        """
        Look up companies by Bloomberg symbols.

        The return value is a dict with the input values as keys and with the corresponding Entity
        objects as values. Symbols which did not return any results, are not included.
        """
        return self._company_by_field("bloomberg_symbol", *symbols)

    def company_by_figi(self, *symbols: str) -> Mapping[str, Entity]:
        """
        Look up companies by FIGI (Financial Instrument Global Identifier).

        The return value is a dict with the input values as keys and with the corresponding Entity
        objects as values. Symbols which did not return any results, are not included.
        """
        return self._company_by_field("figi", *symbols)

    def company_by_factset_identifier(self, *identifiers: str) -> Mapping[str, Entity]:
        """
        Look up companies by FactSet identifiers.

        The return value is a dict with the input values as keys and with the corresponding Entity
        objects as values. Identifiers which did not return any results, are not included.
        """
        return self._company_by_field("factset_identifier", *identifiers)

    def companies_by_text(self, *texts: str) -> Mapping[str, Sequence[Entity]]:
        """
        Search for companies based on text search.

        The method searches for ISINs, tickers and company names, and if the search term is
        sufficiently long, a prefix search is performed.

        A maximum of five companies is returned for each search.

        The return value is a dict with the input values as keys and with a sequence of Entity
        objects as values. Search terms which did not return any results, are not included.
        """
        return self._companies_by_field("text", *texts)

    def company_by_mic_and_ticker(
        self, *mic_and_ticker: Tuple[str, str]
    ) -> Mapping[Tuple[str, str], Entity]:
        """
        Look up companies by MIC (Market Identifier Code) and ticker.

        The return value is a dict with the input values as keys and with the corresponding Entity
        objects as values. MICs and tickers which did not return any results, are not included.
        """
        return self._by_mic_and_ticker(_COMPANY_ENTITY_TYPE, *mic_and_ticker)

    def security_by_mic_and_ticker(
        self, *mic_and_ticker: Tuple[str, str]
    ) -> Mapping[Tuple[str, str], Entity]:
        """
        Look up securities by MIC (Market Identifier Code) and ticker.

        The return value is a dict with the input values as keys and with the corresponding Entity
        objects as values. MICs and tickers which did not return any results, are not included.
        """
        return self._by_mic_and_ticker(_SECURITY_ENTITY_TYPE, *mic_and_ticker)

    def listing_by_mic_and_ticker(
        self, *mic_and_ticker: Tuple[str, str]
    ) -> Mapping[Tuple[str, str], Entity]:
        """
        Look up listings by MIC (Market Identifier Code) and ticker.

        The return value is a dict with the input values as keys and with the corresponding Entity
        objects as values. MICs and tickers which did not return any results, are not included.
        """
        return self._by_mic_and_ticker(_LISTING_ENTITY_TYPE, *mic_and_ticker)

    def entities_by_terms(
        self, entity_type: str, terms: Sequence[Union[SearchTerm, Tuple[str, str]]]
    ) -> Sequence[SearchEntitiesResponse.SearchResult]:
        """
        Look up entities of a given type based on a series of search terms.

        The searches that are performed are determined by the input terms. In most cases one search
        term defines a single query. The exception to this are the 'MIC' and 'ticker' fields, which
        must come in pairs, with 'MIC' immediately before 'ticker'. One such pair is treated as one
        search query.

        The return value contains one SearchResult for every query.
        """
        request = SearchEntitiesRequest(
            parent=entity_type,
            terms=[
                term if isinstance(term, SearchTerm) else SearchTerm(field=term[0], query=term[1])
                for term in terms
            ],
        )
        response = self.client.search_entities(request)
        return response.results

    def _company_by_field(self, field: str, *values: str) -> Mapping[str, Entity]:
        return self._single_result(self._companies_by_field(field, *values))

    def _companies_by_field(self, field: str, *values: str) -> Mapping[str, Sequence[Entity]]:
        return self._by_field(_COMPANY_ENTITY_TYPE, field, *values)

    def _security_by_field(self, field: str, *values: str) -> Mapping[str, Entity]:
        return self._single_result(self._by_field(_SECURITY_ENTITY_TYPE, field, *values))

    def _by_mic_and_ticker(
        self, entity_type: str, *mic_and_ticker: Tuple[str, str]
    ) -> Mapping[Tuple[str, str], Entity]:
        results = self._by_fields(entity_type, ("mic", "ticker"), *itertools.chain(*mic_and_ticker))
        return self._single_result(results)  # type: ignore[arg-type]

    def _single_result(self, results: Mapping[TKey, Sequence[Entity]]) -> Mapping[TKey, Entity]:
        new_results = {}
        for key, value in results.items():
            assert len(value) == 1
            new_results[key] = value[0]
        return new_results

    def _by_field(
        self, entity_type: str, field: str, *values: str
    ) -> Mapping[str, Sequence[Entity]]:
        result: Mapping[Tuple[str, ...], Sequence[Entity]] = self._by_fields(
            entity_type, [field], *values
        )
        return {query[0]: entities for query, entities in result.items()}

    def _by_fields(
        self, entity_type: str, fields: Sequence[str], *values: str
    ) -> Mapping[Tuple[str, ...], Sequence[Entity]]:
        if not values:
            raise ValueError("No search terms provided.")
        tuples = []
        for field, value in zip(itertools.cycle(fields), values):
            tuples.append((field, value))
        results = self.entities_by_terms(entity_type, tuples)
        to_return = {}
        for result in results:
            assert len(result.terms) == len(fields)
            assert list(fields) == [
                term.field for term in result.terms
            ], f"{fields} != {[term.field for term in result.terms]}"
            if result.entities:
                to_return[tuple(term.query for term in result.terms)] = [
                    Entity.from_proto(e) for e in result.entities
                ]
        return to_return
