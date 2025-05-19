import pytest
from fastapi.testclient import TestClient
from main import app
import os
from unittest.mock import patch, AsyncMock
from myOrm import get_db_session
from myDependencies.auth import validate_is_admin


@pytest.fixture(scope="session")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        "AWS_BUCKET_NAME": "test-bucket",
        "AWS_ACCESS_KEY_ID": "test-access-key",
        "AWS_SECRET_ACCESS_KEY": "test-secret-key",
        "AWS_REGION": "us-east-1"
    }):
        yield

@pytest.fixture(autouse=True)
def mock_aws_credentials():
    """Mock AWS credentials for testing"""
    with patch('boto3.client') as mock_boto3:
        mock_s3 = mock_boto3.return_value
        mock_s3.generate_presigned_url.return_value = "https://test-bucket.s3.amazonaws.com/test-image.jpg"
        yield mock_s3

@pytest.fixture
def mock_db_session():
    """Mock database session for testing"""
    mock_session = AsyncMock()
    mock_session.get = AsyncMock()
    mock_session.add = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    mock_session.delete = AsyncMock()
    return mock_session

@pytest.fixture
def mock_admin_user():
    """Mock admin user for testing"""
    from myOrm.models import Client
    return Client(id=1, is_admin=True)

@pytest.fixture(autouse=True)
def override_dependencies(mock_db_session, mock_admin_user):
    # make a dependency that yields your mock session
    async def override_get_db_session():
        yield mock_db_session

    # shortcut admin‐check to always return your mock_admin_user
    def override_validate_is_admin():
        return mock_admin_user

    app.dependency_overrides = {
        get_db_session: override_get_db_session,
        validate_is_admin: override_validate_is_admin,
    }
    yield
    app.dependency_overrides = {}
