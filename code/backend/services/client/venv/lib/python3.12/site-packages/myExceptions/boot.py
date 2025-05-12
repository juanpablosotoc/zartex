class BootError(Exception):
    """Raised when a boot error occurs."""
    pass

class ConfigurationError(BootError):
    """Raised when a configuration error occurs."""
    pass
