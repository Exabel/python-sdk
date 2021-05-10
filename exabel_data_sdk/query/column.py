from dataclasses import dataclass
from typing import Optional

from exabel_data_sdk.query.comparison import Comparison
from exabel_data_sdk.query.in_predicate import InPredicate
from exabel_data_sdk.query.literal import Literal, escape


@dataclass
class Column:

    name: str
    expression: Optional[str] = None

    def sql(self) -> str:
        """Returns the SQL representation of this column as used in the SELECT part."""
        if self.expression:
            return f"{escape(self.expression)} AS {self.name}"
        return self.name

    def eq(self, value: Literal) -> Comparison:
        return Comparison(self.name, "=", value)

    def less_eq(self, value: Literal) -> Comparison:
        return Comparison(self.name, "<=", value)

    def greater_eq(self, value: Literal) -> Comparison:
        return Comparison(self.name, ">=", value)

    def in_list(self, *values: Literal) -> InPredicate:
        return InPredicate(self.name, values)
