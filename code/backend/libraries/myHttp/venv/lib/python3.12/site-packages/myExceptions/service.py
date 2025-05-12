class ServiceError(Exception):
    """Base class for all service-related exceptions."""
    pass

class ResourceNotFoundError(ServiceError):
    """Raised when a requested resource is not found."""
    pass

class BusinessLogicError(ServiceError):
    """Raised when a business rule or constraint is violated."""
    pass

class ExternalServiceError(ServiceError):
    """Raised when there are issues with external service integrations."""
    pass

class ConfigurationError(ServiceError):
    """Raised when there are issues with service configuration."""
    pass 