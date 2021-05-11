from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

from exabel_data_sdk.query.literal import Literal, to_sql


class Predicate(ABC):
    """
    Represents a condition that needs to be satisfied for the rows to be included.
    One or several predicates are used as the WHERE part of a query.
    """

    @abstractmethod
    def sql(self) -> str:
        """Returns the SQL representation of this predicate."""


@dataclass
class Comparison(Predicate):
    """
    A predicate where a column value is compared to a literal value.
    The comparison operator would typically be =, <= or >=.
    """

    column: str
    operator: str
    value: Literal

    def sql(self) -> str:
        return f"{self.column} {self.operator} {to_sql(self.value)}"


@dataclass
class InPredicate(Predicate):
    """A predicate where a column takes one of several provided values."""

    column: str
    values: Sequence[Literal]

    def sql(self) -> str:
        return f"{self.column} IN ({', '.join([to_sql(value) for value in self.values])})"


@dataclass
class FunctionPredicate(Predicate):
    """A predicate which is a function call."""

    function: str
    arguments: Sequence[Literal]

    def sql(self) -> str:
        return f"{self.function}({', '.join([to_sql(value) for value in self.arguments])})"
