from dataclasses import dataclass
from typing import Sequence

from exabel.query.column import Column
from exabel.query.predicate import Predicate
from exabel.query.table import Table


@dataclass
class Query:
    """
    Represents a SELECT query to the data API.
    """

    # The table to retrieve data from
    table: Table

    # The columns to retrieve
    columns: Sequence[Column]

    # The WHERE part of the query
    predicates: Sequence[Predicate]

    def sql(self) -> str:
        """Returns the query string"""
        cols = ", ".join([col.sql() for col in self.columns])
        query = f"SELECT {cols} FROM {self.table.name}"
        if self.predicates:
            query += " WHERE " + " AND ".join([p.sql() for p in self.predicates])
        return query
