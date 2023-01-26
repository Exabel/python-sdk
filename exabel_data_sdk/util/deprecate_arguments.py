import functools
import warnings
from typing import Any, Callable, Optional, TypeVar, overload

from exabel_data_sdk.util.warnings import ExabelDeprecationWarning

FunctionT = TypeVar("FunctionT", bound=Callable[..., Any])

# Pylint flags '__func' as an invalid argument name, but we want the '__' prefix to make Mypy
# interpret it as a positional-only argument. Therefore, we disable the check for this argument.
@overload
def deprecate_arguments(
    **deprecation_replacements: Optional[str],
) -> Callable[[FunctionT], FunctionT]:
    ...


@overload
def deprecate_arguments(
    __func: None,  # pylint: disable=invalid-name
    **deprecation_replacements: Optional[str],
) -> Callable[[FunctionT], FunctionT]:
    ...


@overload
def deprecate_arguments(
    __func: FunctionT,  # pylint: disable=invalid-name
    **deprecation_replacements: Optional[str],
) -> FunctionT:
    ...


def deprecate_arguments(
    __func: Optional[FunctionT] = None,  # pylint: disable=invalid-name
    **deprecation_replacements: Optional[str],
) -> FunctionT:
    """
    Decorator for warning about and replacing deprecated arguments in a function that will be
    removed in a future release.

    Only works for deprecating [keyword-only arguments](https://peps.python.org/pep-3102/).

    Args:
        deprecation_replacements: a mapping from deprecated argument names to the new argument
            names or `None` if the argument has been removed and no longer serves any purpose.
    """

    if not deprecation_replacements:
        raise ValueError("No deprecations specified")

    def decorator(func: FunctionT) -> FunctionT:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__qualname__
            module_name = func.__module__
            if module_name != "__main__":
                func_name = f"{module_name}.{func_name}"
            new_kwargs = {}
            for arg_name, arg_value in kwargs.items():
                if arg_name in deprecation_replacements:
                    warning_message = (
                        f"Argument '{arg_name}' is deprecated in '{func_name}' and will be removed "
                        "in a future release. "
                    )
                    replacement = deprecation_replacements[arg_name]
                    if replacement:
                        if replacement in kwargs:
                            raise ValueError(
                                f"Cannot specify both '{arg_name}' and '{replacement}' in "
                                f"'{func_name}'."
                            )
                        new_kwargs[replacement] = arg_value
                        warning_message += f"Use '{replacement}' instead."
                    warnings.warn(
                        warning_message,
                        ExabelDeprecationWarning,
                    )
                else:
                    new_kwargs[arg_name] = arg_value
            return func(*args, **new_kwargs)

        return wrapper  # type: ignore[return-value]

    if __func:
        return decorator(__func)
    return decorator  # type: ignore[return-value]
