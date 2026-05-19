"""Resolve company resource names with the SDK's entity search helpers.

Most Data API calls take a resource_name like
entityTypes/company/entities/F_XXXXXX-E.
The SDK exposes a search service on client.entity_api.search that maps
common external identifiers onto the matching entity.

This example demonstrates the three lookups callers reach for most:

1. By Bloomberg ticker — exact, returns one entity per ticker.
2. By MIC and ticker — disambiguates a plain ticker across exchanges.
3. By free text — fuzzy match across name and ticker fields, sorted by
   relevance. Returns multiple candidates per query.

See client.api.search_service for other search methods.
"""

from pprint import pprint

from exabel import ExabelClient


def main() -> None:
    """Run the three search variants and pretty-print the raw mappings each returns."""
    client = ExabelClient()

    print("\n# Bloomberg ticker")
    pprint(client.entity_api.search.company_by_bloomberg_ticker("AAPL US", "GOOGL US"))

    print("\n# MIC and ticker")
    pprint(
        client.entity_api.search.company_by_mic_and_ticker(
            ("XNAS", "AAPL"),
            ("XNAS", "GOOGL"),
        )
    )

    print("\n# Free text (fuzzy, can match multiple candidates per query)")
    pprint(client.entity_api.search.companies_by_text("Apple, Inc.", "Alphabet"))


if __name__ == "__main__":
    main()
