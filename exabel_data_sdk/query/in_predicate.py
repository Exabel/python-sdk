from dataclasses import dataclass
from typing import Sequence

from exabel_data_sdk.query.literal import Literal, to_sql
from exabel_data_sdk.query.predicate import Predicate


@dataclass
class InPredicate(Predicate):
    """"""

    column: str
    values: Sequence[Literal]

    def sql(self) -> str:
        return f"{self.column} IN ({', '.join([to_sql(value) for value in self.values])})"
