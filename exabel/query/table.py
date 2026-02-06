from dataclasses import dataclass


@dataclass
class Table:
    """Represents a table available for querying through the Exabel API."""

    # The name of the table
    name: str
