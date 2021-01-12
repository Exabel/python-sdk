from typing import Mapping, Union

from google.protobuf.struct_pb2 import Struct


def from_struct(struct: Struct) -> Mapping[str, Union[str, bool, int, float]]:
    """
    Convert a protobuf Struct into a Dict.
    """
    for value in struct.values():
        if not isinstance(value, (str, bool, int, float)):
            raise ValueError(f"Struct contains unsupported value: {value}")
    return dict(struct.items())


def to_struct(values: Mapping[str, Union[str, bool, int, float]]) -> Struct:
    """
    Convert a Dict into a protobuf Struct.
    """
    struct = Struct()
    struct.update(values)
    return struct
