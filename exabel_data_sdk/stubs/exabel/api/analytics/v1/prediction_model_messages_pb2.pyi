"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright (c) 2022 Exabel AS. All rights reserved."""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing
if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _ModelConfiguration:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ModelConfigurationEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ModelConfiguration.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    MODEL_CONFIGURATION_NOT_SPECIFIED: _ModelConfiguration.ValueType
    'Not specified - defaults to use the latest configuration.'
    LATEST: _ModelConfiguration.ValueType
    'Latest configuration.'
    ACTIVE: _ModelConfiguration.ValueType
    'Configuration of the active run. A specific run may be activated from the prediction model user interface.'
    SPECIFIC_RUN: _ModelConfiguration.ValueType
    'Configuration of a specific run. The run number must be specified as well.'

class ModelConfiguration(_ModelConfiguration, metaclass=_ModelConfigurationEnumTypeWrapper):
    """Specifies which model configuration to use. If not specified, the latest model configuration is used.
    Note that the current signal library is always loaded.
    """
MODEL_CONFIGURATION_NOT_SPECIFIED: ModelConfiguration.ValueType
'Not specified - defaults to use the latest configuration.'
LATEST: ModelConfiguration.ValueType
'Latest configuration.'
ACTIVE: ModelConfiguration.ValueType
'Configuration of the active run. A specific run may be activated from the prediction model user interface.'
SPECIFIC_RUN: ModelConfiguration.ValueType
'Configuration of a specific run. The run number must be specified as well.'
global___ModelConfiguration = ModelConfiguration

@typing.final
class PredictionModelRun(google.protobuf.message.Message):
    """A prediction model run."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    CONFIGURATION_FIELD_NUMBER: builtins.int
    CONFIGURATION_SOURCE_FIELD_NUMBER: builtins.int
    AUTO_ACTIVATE_FIELD_NUMBER: builtins.int
    name: builtins.str
    'Unique resource name of the run, e.g. `predictionModels/123/runs/3`.'
    description: builtins.str
    'You may use this to record some notes about the run. This is shown in the prediction model\n    interface when viewing all runs, and when viewing the results of a single run.\n    '
    configuration: global___ModelConfiguration.ValueType
    'Which model configuration to use. If not specified, the latest model configuration is used.\n    Note that the current signal library is always loaded.\n    '
    configuration_source: builtins.int
    'Prediction model run number from which model configuration should be retrieved, e.g. `1`.\n    Only relevant when `configuration` is set to `ModelConfiguration.SPECIFIC_RUN`.\n    '
    auto_activate: builtins.bool
    'Whether to automatically set this run as active once it completes.\n    The run will not be activated if it fails for any of the entities in the model.\n    '

    def __init__(self, *, name: builtins.str | None=..., description: builtins.str | None=..., configuration: global___ModelConfiguration.ValueType | None=..., configuration_source: builtins.int | None=..., auto_activate: builtins.bool | None=...) -> None:
        ...

    def HasField(self, field_name: typing.Literal['_configuration_source', b'_configuration_source', 'configuration_source', b'configuration_source']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing.Literal['_configuration_source', b'_configuration_source', 'auto_activate', b'auto_activate', 'configuration', b'configuration', 'configuration_source', b'configuration_source', 'description', b'description', 'name', b'name']) -> None:
        ...

    def WhichOneof(self, oneof_group: typing.Literal['_configuration_source', b'_configuration_source']) -> typing.Literal['configuration_source'] | None:
        ...
global___PredictionModelRun = PredictionModelRun