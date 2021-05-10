from dataclasses import dataclass

from exabel_data_sdk.query.literal import Literal, to_sql
from exabel_data_sdk.query.predicate import Predicate


@dataclass
class Comparison(Predicate):
    """"""

    column: str
    operator: str
    value: Literal

    def sql(self) -> str:
        return f"{self.column} {self.operator} {to_sql(self.value)}"
