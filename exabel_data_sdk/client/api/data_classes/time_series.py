from __future__ import annotations

from dataclasses import dataclass


def _invalid_time_series_name(name: str) -> ValueError:
    return ValueError(
        f"Unable to parse time series name: {name}. Should contain 6 parts on the canonical form: "
        "entityTypes/<entityType>/entities/<entity>/signals/<signal> or the alternative form: "
        "signals/<signal>/entityTypes/<entityType>/entities/<entity>"
    )


@dataclass(frozen=True)
class TimeSeriesResourceName:
    """Represents a time series resource name."""

    entity_type: str
    entity: str
    signal: str

    @property
    def entity_name(self) -> str:
        """Get the entity name."""
        return f"entityTypes/{self.entity_type}/entities/{self.entity}"

    @property
    def signal_name(self) -> str:
        """Get the signal name."""
        return f"signals/{self.signal}"

    @property
    def canonical_name(self) -> str:
        """The canonical name of the time series."""
        return f"{self.entity_name}/{self.signal_name}"

    @classmethod
    def from_string(cls, name: str) -> TimeSeriesResourceName:
        """Create a time series resource name from a string."""
        ts_name_parts = name.split("/")
        if len(ts_name_parts) != 6:
            raise _invalid_time_series_name(name)
        if (ts_name_parts[0], ts_name_parts[2], ts_name_parts[4]) == (
            "entityTypes",
            "entities",
            "signals",
        ):
            entity_type = ts_name_parts[1]
            entity = ts_name_parts[3]
            signal = ts_name_parts[5]
        elif (ts_name_parts[0], ts_name_parts[2], ts_name_parts[4]) == (
            "signals",
            "entityTypes",
            "entities",
        ):
            signal = ts_name_parts[1]
            entity_type = ts_name_parts[3]
            entity = ts_name_parts[5]
        else:
            raise _invalid_time_series_name(name)
        return cls(entity_type, entity, signal)
