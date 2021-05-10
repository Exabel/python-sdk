from abc import ABC, abstractmethod


class Predicate(ABC):
    """"""

    @abstractmethod
    def sql(self) -> str:
        """Returns the SQL representation of this filter."""
