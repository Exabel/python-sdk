import argparse
import warnings
from typing import Sequence, Union

from exabel_data_sdk.util.warnings import ExabelDeprecationWarning


class DeprecatedArgumentAction(argparse.Action):
    """
    Argparse action for deprecated command line arguments.

    If the deprecated argument is being replaced by another argument, put the new argument together
    with this action in a mutually exclusive group. This will ensure that the user does not specify
    both arguments. If the deprecated argument is being replaced by no argument, set the
    `replace_with_none` argument to `True` when using this action.
    """

    def __init__(  # type: ignore
        self, *args, case_insensitive: bool = False, replace_with_none: bool = False, **kwargs
    ) -> None:
        self._case_insensitive = case_insensitive
        self._replace_with_none = replace_with_none
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None) -> None:  # type: ignore
        warnings.warn(
            f"{option_string} is deprecated and will be removed in a future release",
            ExabelDeprecationWarning,
        )
        if self._case_insensitive:
            values = case_insensitive_argument(values)
        if self._replace_with_none:
            values = None
        setattr(namespace, self.dest, values)


class CaseInsensitiveArgumentAction(argparse.Action):
    """
    Argparse action to lowercase argument values on string or list of string arguments.
    """

    def __call__(self, parser, namespace, values, option_string=None) -> None:  # type: ignore
        values = case_insensitive_argument(values)
        setattr(namespace, self.dest, values)


def case_insensitive_argument(values: Union[str, Sequence, None]) -> Union[str, Sequence, None]:
    """
    Lowercase all argument values that are type `str`.
    """
    if isinstance(values, list):
        assert isinstance(values[0], str), "Case insensitive argument must be a string"
        return [v.lower() for v in values]
    if values is not None:
        assert isinstance(values, str), "Case insensitive argument must be a string"
        return values.lower()
    return values
