from dataclasses import dataclass
from typing import Sequence

from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.predicate import Predicate
from exabel_data_sdk.query.table import Table


@dataclass
class Query:

    table: Table
    columns: Sequence[Column]
    filters: Sequence[Predicate]

    def sql(self) -> str:
        cols = ", ".join([col.sql() for col in self.columns])
        query = f"SELECT {cols} FROM {self.table.name}"
        if self.filters:
            query += " WHERE " + " AND ".join([f.sql() for f in self.filters])
        return query
