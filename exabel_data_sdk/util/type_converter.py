from typing import Union

from exabel_data_sdk.util.exceptions import TypeConvertionError


def type_converter(value: str, type_: type) -> Union[str, int, float, bool]:
    """
    Convert a string value to the given type.
    """
    try:
        if type_ is str:
            return value
        if type_ is int:
            return int(value)
        if type_ is float:
            return float(value)
        if type_ is bool:
            if value.lower() == "true":
                return True
            if value.lower() == "false":
                return False
            raise ValueError(f"Invalid boolean value: '{value}', expected 'true' or 'false'")
    except ValueError as e:
        raise TypeConvertionError(f"Unable to convert '{value}' to {type_}") from e
    raise TypeConvertionError(f"Unsupported type: {type_}")
