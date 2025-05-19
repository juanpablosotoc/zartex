import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch, MagicMock
from myDependencies.auth import validate_is_authenticated, validate_is_admin
from myOrm import Client
from jwt.exceptions import InvalidTokenError

@pytest.fixture
def mock_db_session():
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result
    return mock_session

@pytest.fixture
def mock_client():
    client = Client()
    client.id = 1
    client.is_admin = False
    return client

@pytest.mark.asyncio
async def test_validate_is_authenticated_success(mock_db_session, mock_client):
    # Arrange
    valid_token = "valid_token"
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_client
    mock_db_session.execute.return_value = mock_result
    
    async def mock_db_gen():
        yield mock_db_session

    with patch('myDependencies.auth.Encryption.verify_token') as mock_verify:
        mock_verify.return_value = {"user_id": 1}
        
        # Act
        result = await validate_is_authenticated(token=valid_token, db_async_gen=mock_db_gen())
        
        # Assert
        assert result == mock_client
        mock_verify.assert_called_once_with(valid_token)
        mock_db_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_validate_is_authenticated_invalid_token(mock_db_session):
    # Arrange
    invalid_token = "invalid_token"
    
    async def mock_db_gen():
        yield mock_db_session

    with patch('myDependencies.auth.Encryption.verify_token') as mock_verify:
        mock_verify.side_effect = InvalidTokenError()
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await validate_is_authenticated(token=invalid_token, db_async_gen=mock_db_gen())
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid token"

@pytest.mark.asyncio
async def test_validate_is_authenticated_user_not_found(mock_db_session):
    # Arrange
    valid_token = "valid_token"
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_session.execute.return_value = mock_result
    
    async def mock_db_gen():
        yield mock_db_session

    with patch('myDependencies.auth.Encryption.verify_token') as mock_verify:
        mock_verify.return_value = {"user_id": 1}
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await validate_is_authenticated(token=valid_token, db_async_gen=mock_db_gen())
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid token"

@pytest.mark.asyncio
async def test_validate_is_admin_success(mock_client):
    # Arrange
    mock_client.is_admin = True
    
    # Act
    result = await validate_is_admin(user=mock_client)
    
    # Assert
    assert result == mock_client

@pytest.mark.asyncio
async def test_validate_is_admin_unauthorized(mock_client):
    # Arrange
    mock_client.is_admin = False
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await validate_is_admin(user=mock_client)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not authorized to access this resource" 