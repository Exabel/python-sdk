from typing import Mapping, MutableMapping

from exabel_data_sdk.util.exceptions import ParsePropertyColumnsError


def parse_property_columns(*property_columns: str) -> Mapping[str, type]:
    """
    Parse the property columns and return a mapping of column names to data types.
    """
    if not property_columns:
        return {}
    property_columns_map: MutableMapping[str, type] = {}
    for column_name_and_type in property_columns:
        try:
            column_name, column_type = column_name_and_type.split(":", 1)
        except ValueError as e:
            raise ParsePropertyColumnsError(
                f"Missing column type for column '{column_name_and_type}'"
            ) from e
        if column_type == "bool":
            property_columns_map[column_name] = bool
        elif column_type == "str":
            property_columns_map[column_name] = str
        elif column_type == "int":
            property_columns_map[column_name] = int
        elif column_type == "float":
            property_columns_map[column_name] = float
        else:
            raise ParsePropertyColumnsError(
                f"Invalid property type '{column_type}' for column '{column_name}'"
            )
    return property_columns_map
