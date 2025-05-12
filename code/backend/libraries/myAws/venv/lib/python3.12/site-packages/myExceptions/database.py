class DatabaseError(Exception):
    """Base class for all database-related exceptions."""
    pass

class ConnectionError(DatabaseError):
    """Raised when there are issues connecting to the database."""
    pass

class QueryError(DatabaseError):
    """Raised when there are issues with database queries."""
    pass

class RecordNotFoundError(DatabaseError):
    """Raised when a requested record is not found in the database."""
    pass

class DuplicateRecordError(DatabaseError):
    """Raised when attempting to create a record that already exists."""
    pass 