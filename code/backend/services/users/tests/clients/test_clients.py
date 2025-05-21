# tests/test_clients.py
import pytest
from datetime import datetime
from myEncryption import Encryption
from myOrm.models import Client as ClientModel
from tests.helpers import TEST_CLIENT_ID, TEST_EMAIL, TEST_FIRST_NAME, TEST_LAST_NAME, TEST_PASSWORD, DummyResult


@pytest.mark.asyncio
async def test_create_client_success(test_client, mock_db_session):
    # Simulate no existing email check
    mock_db_session.execute.return_value = DummyResult(None)
    # Simulate refresh() populating id, created_at, is_afiliado
    def refresh_side_effect(instance):
        instance.id = TEST_CLIENT_ID
        instance.created_at = datetime.utcnow()
        instance.is_afiliado = False
    mock_db_session.refresh.side_effect = refresh_side_effect

    payload = {
        "email": TEST_EMAIL,
        "first_name": TEST_FIRST_NAME,
        "last_name": TEST_LAST_NAME,
        "password": TEST_PASSWORD
    }
    response = test_client.post(
        "/api/v1/users/clients/",
        json=payload
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == TEST_CLIENT_ID
    assert body["email"] == TEST_EMAIL
    assert body["first_name"] == TEST_FIRST_NAME
    assert body["last_name"] == TEST_LAST_NAME
    assert body.get("is_afiliado") is False

@pytest.mark.asyncio
async def test_get_me_success(test_client, mock_admin_user):
    # Ensure authenticated user has created_at
    mock_admin_user.created_at = datetime.utcnow()
    token = Encryption.generate_token({"user_id": mock_admin_user.id, "role": "user"})
    response = test_client.get(
        "/api/v1/users/clients/me",
        headers={"token": token}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == mock_admin_user.id
    assert body["email"] == mock_admin_user.email

@pytest.mark.asyncio
async def test_delete_me_success(test_client, mock_admin_user):
    mock_admin_user.created_at = datetime.utcnow()
    token = Encryption.generate_token({"user_id": mock_admin_user.id, "role": "user"})
    response = test_client.delete(
        "/api/v1/users/clients/me",
        headers={"token": token}
    )
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_update_me_success(test_client, mock_admin_user):
    mock_admin_user.created_at = datetime.utcnow()
    new_name = "Updated"
    payload = {"first_name": new_name}
    token = Encryption.generate_token({"user_id": mock_admin_user.id, "role": "user"})
    response = test_client.put(
        "/api/v1/users/clients/me",
        json=payload,
        headers={"token": token}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["first_name"] == new_name

@pytest.mark.asyncio
async def test_get_client_success(test_client, mock_db_session, create_test_client, mock_admin_user):
    # Admin access to get another client by ID
    mock_db_session.execute.return_value = DummyResult(create_test_client)
    token = Encryption.generate_token({"user_id": mock_admin_user.id, "role": "admin"})
    response = test_client.get(
        f"/api/v1/users/clients/{TEST_CLIENT_ID}",
        headers={"token": token}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == TEST_CLIENT_ID
    assert body["email"] == TEST_EMAIL

@pytest.mark.asyncio
async def test_get_client_not_found(test_client, mock_db_session, mock_admin_user):
    mock_db_session.execute.return_value = DummyResult(None)
    token = Encryption.generate_token({"user_id": mock_admin_user.id, "role": "admin"})
    response = test_client.get(
        f"/api/v1/users/clients/{TEST_CLIENT_ID}",
        headers={"token": token}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"
