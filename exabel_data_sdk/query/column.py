from dataclasses import dataclass
from typing import Optional

from exabel_data_sdk.query.literal import Literal, escape
from exabel_data_sdk.query.predicate import Comparison, InPredicate


@dataclass
class Column:
    """
    Represents a column in a table.

    Can take one of two forms:
     - If only 'name' is provided, it refers to a known column with that name
     - If both 'expression' and 'name' are provided, it defines a new column
       that is to be calculated using the expression and given the provided name.
    """

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
