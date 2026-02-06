class TypeConversionError(Exception):
    """Represents an error that occurred during type conversion."""


# Misspelled class name as an alias for backwards compatibility.
TypeConvertionError = TypeConversionError


class ParsePropertyColumnsError(Exception):
    """Represents an error that occurred during parsing of property columns."""


class NoWriteableNamespaceError(Exception):
    """Represents an error that occurred when no writeable namespace exists."""
