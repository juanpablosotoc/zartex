class ValidationError(Exception):
    """Base class for all validation-related exceptions."""
    pass

class InvalidInputError(ValidationError):
    """Raised when input data is invalid or malformed."""
    pass

class RequiredFieldError(ValidationError):
    """Raised when a required field is missing."""
    pass

class InvalidFormatError(ValidationError):
    """Raised when data format is invalid (e.g., invalid email format, date format)."""
    pass 