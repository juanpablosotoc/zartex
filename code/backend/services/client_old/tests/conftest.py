import pytest
import os
from config import Config


# Configure pytest-asyncio
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as async"
    )


@pytest.fixture(autouse=True)
def setup_test_environment():
    """
    Setup test environment variables and configurations.
    This fixture runs automatically for all tests.
    """
    # Set test JWT secret key
    os.environ['JWT_SECRET_KEY'] = 'test_secret_key'
    Config.JWT_SECRET_KEY = 'test_secret_key'
    Config.JWT_ALGORITHM = 'HS256'
    
    # Set test AWS configuration
    os.environ['AWS_BUCKET_NAME'] = 'test-bucket'
    
    yield
    
    # Cleanup after tests
    if 'JWT_SECRET_KEY' in os.environ:
        del os.environ['JWT_SECRET_KEY']
    if 'AWS_BUCKET_NAME' in os.environ:
        del os.environ['AWS_BUCKET_NAME']


