class AuthenticationError(Exception):
    """Base class for all authentication-related exceptions."""
    pass

class InvalidCredentialsError(AuthenticationError):
    """Raised when the provided credentials (username/password) are invalid."""
    pass

class TokenError(AuthenticationError):
    """Raised when there are issues with authentication tokens (expired, invalid, missing)."""
    pass

class PermissionError(AuthenticationError):
    """Raised when a user doesn't have the required permissions to perform an action."""
    pass

class AccountStatusError(AuthenticationError):
    """Raised when there are issues with the account status (locked, disabled, etc.)."""
    pass
