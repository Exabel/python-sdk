class SqlError(Exception):
    """Raised when an error occurs in a SQL service."""


class InvalidServiceAccountCredentialsError(SqlError):
    """Raised when service account credentials cannot be parsed."""
