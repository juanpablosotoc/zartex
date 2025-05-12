from fastapi import HTTPException


class HTTPError(HTTPException):
    """Base class for all HTTP-related exceptions."""
    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        super().__init__(status_code=status_code, detail=message)

class BadRequestError(HTTPError):
    """Raised for 400 Bad Request errors."""
    def __init__(self, message: str = "Bad Request"):
        super().__init__(message, 400)

class UnauthorizedError(HTTPError):
    """Raised for 401 Unauthorized errors."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)

class ForbiddenError(HTTPError):
    """Raised for 403 Forbidden errors."""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, 403)

class NotFoundError(HTTPError):
    """Raised for 404 Not Found errors."""
    def __init__(self, message: str = "Not Found"):
        super().__init__(message, 404)

class ConflictError(HTTPError):
    """Raised for 409 Conflict errors."""
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, 409)

class InternalServerError(HTTPError):
    """Raised for 500 Internal Server errors."""
    def __init__(self, message: str = "Internal Server Error"):
        super().__init__(message, 500) 
