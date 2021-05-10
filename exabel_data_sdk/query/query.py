from typing import Sequence

from dataclasses import dataclass

from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.filter import Filter
from exabel_data_sdk.query.table import Table


@dataclass
class Query:

    table: Table
    columns: Sequence[Column]
    filters: Sequence[Filter]

    def sql(self) -> str:
        cols = ", ".join([col.sql() for col in self.columns])
        query = f"SELECT {cols} FROM {self.table.name}"
        if self.filters:
            query += " WHERE " + " AND ".join([f.sql() for f in self.filters])
        return query
