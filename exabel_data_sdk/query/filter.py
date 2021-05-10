from abc import ABC, abstractmethod
from typing import Union

from dataclasses import dataclass

from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.util import escape

Term = Union[Column, str, int, float]


def to_sql(term: Term) -> str:
    """Returns the SQL representation of the given term."""
    if isinstance(term, Column):
        return term.name
    if isinstance(term, str):
        return escape(term)
    if isinstance(term, (Column, int, float)):
        return str(term)
    raise ValueError(f"Unknown object type {type(term)} for {term}")


class Filter(ABC):
    """"""

    @staticmethod
    def eq(left: Term, right: Term) -> 'Filter':
        return RelationFilter(left, right, "=")

    @abstractmethod
    def sql(self) -> str:
        """Returns the SQL representation of this filter."""


@dataclass
class RelationFilter(Filter):
    """"""

    left: Term
    right: Term
    operation: str

    def sql(self) -> str:
        return f"{to_sql(self.left)} {self.operation} {to_sql(self.right)}"
