import sys

from .client.exabel_client import ExabelClient

if sys.version_info.major == 3 and sys.version_info.minor == 6:
    import warnings

    warnings.warn(
        "Python 3.6 is deprecated as of version 3.3.0 of the Exabel Python SDK. Support will be "
        "removed in a future release. Please upgrade to Python 3.7 or a newer release of Python.",
        FutureWarning,
    )
