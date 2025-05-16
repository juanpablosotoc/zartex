class ValidationError(Exception):
    """Base class for all validation-related exceptions."""
    pass

class FileNotFoundError(ValidationError):
    """
    Raised when a file is not found.
    """
    status_code: int = 404
    error_code: str = 'file_not_found'
    message: str = "File not found."

class FileAlreadyExistsError(ValidationError):
    """
    Raised when a file already exists.
    """
    status_code: int = 409
    error_code: str = 'file_already_exists'
    message: str = "File already exists."

class InvalidInputError(ValidationError):
    """Raised when input data is invalid or malformed."""
    pass

class RequiredFieldError(ValidationError):
    """Raised when a required field is missing."""
    pass

class InvalidFormatError(ValidationError):
    """Raised when data format is invalid (e.g., invalid email format, date format)."""
    pass 

class ValueOutOfRangeError(ValidationError):
    """
    Raised when a value is out of the allowed range.
    """
    error_code: str = 'value_out_of_range'
    message: str = "Input value is out of the allowed range."
    