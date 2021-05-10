from typing import Optional

from dataclasses import dataclass

from exabel_data_sdk.query.util import escape


@dataclass
class Column:

    name: str
    expression: Optional[str] = None

    def sql(self) -> str:
        """Returns the SQL representation of this column as used in the SELECT part."""
        if self.expression:
            return f"{escape(self.expression)} AS {self.name}"
        return self.name
