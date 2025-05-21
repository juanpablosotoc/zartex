import pytest
from datetime import datetime
from myOrm.models import Address as AddressModel
from tests.helpers import TEST_CLIENT_ID, DummyResult


@ pytest.mark.asyncio
async def test_create_address_success(test_client, mock_db_session, create_test_client):
    # Simulate existing client check
    mock_db_session.execute.return_value = DummyResult(create_test_client)
    # Simulate refresh() populating id and created_at
    def refresh_side_effect(instance):
        instance.id = 1
        instance.created_at = datetime.utcnow()
    mock_db_session.refresh.side_effect = refresh_side_effect

    payload = {
        "street_address": "123 Main St",
        "city": "Testville",
        "state": "TS",
        "postal_code": "12345",
        "country": "Testland",
        "is_default": False
    }
    response = test_client.post(
        "/api/v1/users/addresses/",
        json=payload
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["client_id"] == TEST_CLIENT_ID
    for key, value in payload.items():
        assert body[key] == value


@ pytest.mark.asyncio
async def test_create_address_client_not_found(test_client, mock_db_session):
    # Simulate client not found
    mock_db_session.execute.return_value = DummyResult(None)
    payload = {
        "street_address": "123 Main St",
        "city": "Testville",
        "state": "TS",
        "postal_code": "12345",
        "country": "Testland",
        "is_default": False
    }
    response = test_client.post(
        "/api/v1/users/addresses/",
        json=payload
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


@ pytest.mark.asyncio
async def test_list_addresses_success(test_client, mock_db_session):
    address = AddressModel(
        id=1,
        client_id=TEST_CLIENT_ID,
        street_address="123 Main St",
        city="Testville",
        state="TS",
        postal_code="12345",
        country="Testland",
        is_default=False
    )
    address.created_at = datetime.utcnow()
    # Simulate list query
    mock_db_session.execute.return_value.scalars.return_value.all.return_value = [address]
    response = test_client.get("/api/v1/users/addresses/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert body[0]["id"] == 1
    assert body[0]["client_id"] == TEST_CLIENT_ID
    assert body[0]["street_address"] == "123 Main St"


@ pytest.mark.asyncio
async def test_list_addresses_empty(test_client, mock_db_session):
    mock_db_session.execute.return_value.scalars.return_value.all.return_value = []
    response = test_client.get("/api/v1/users/addresses/")
    assert response.status_code == 200
    assert response.json() == []


@ pytest.mark.asyncio
async def test_get_address_success(test_client, mock_db_session):
    address = AddressModel(
        id=1,
        client_id=TEST_CLIENT_ID,
        street_address="123 Main St",
        city="Testville",
        state="TS",
        postal_code="12345",
        country="Testland",
        is_default=False
    )
    address.created_at = datetime.utcnow()
    mock_db_session.execute.return_value.scalars.return_value.one_or_none.return_value = address
    response = test_client.get("/api/v1/users/addresses/1")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["client_id"] == TEST_CLIENT_ID
    assert body["street_address"] == "123 Main St"


@ pytest.mark.asyncio
async def test_get_address_not_found(test_client, mock_db_session):
    mock_db_session.execute.return_value.scalars.return_value.one_or_none.return_value = None
    response = test_client.get("/api/v1/users/addresses/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"


@ pytest.mark.asyncio
async def test_delete_address_success(test_client, mock_db_session):
    address = AddressModel(
        id=1,
        client_id=TEST_CLIENT_ID,
        street_address="123 Main St",
        city="Testville",
        state="TS",
        postal_code="12345",
        country="Testland",
        is_default=False
    )
    address.created_at = datetime.utcnow()
    mock_db_session.execute.return_value.scalars.return_value.one_or_none.return_value = address
    response = test_client.delete("/api/v1/users/addresses/1")
    assert response.status_code == 204


@ pytest.mark.asyncio
async def test_delete_address_not_found(test_client, mock_db_session):
    mock_db_session.execute.return_value.scalars.return_value.one_or_none.return_value = None
    response = test_client.delete("/api/v1/users/addresses/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"
