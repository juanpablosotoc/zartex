import pytest
from PIL import Image as PILImage
from io import BytesIO
from unittest.mock import patch
from datetime import datetime
from myEncryption import Encryption
from fastapi import HTTPException

from myOrm.models import Image as ImageModel

# Test constants
TEST_IMAGE_ID = 1
TEST_FILENAME = "test_image.jpg"
TEST_IMAGE_URL = "https://test-bucket.s3.amazonaws.com/test_image.jpg"

@pytest.fixture
def create_test_image():
    """
    Return a small in-memory JPEG for upload.
    """
    buf = BytesIO()
    PILImage.new("RGB", (100, 100), color="red").save(buf, format="JPEG")
    buf.seek(0)
    return buf

@pytest.mark.asyncio
async def test_create_image_success(test_client, mock_db_session, mock_admin_user, create_test_image):
    # Generate admin token
    token = Encryption.generate_token({"user_id": 1, "role": "admin"})

    # Patch S3 to avoid real AWS calls
    with patch("routers.images.views.S3") as mock_s3:
        mock_s3.upload_fileobj.return_value = None
        mock_s3.generate_public_url.return_value = TEST_IMAGE_URL

        # Snapshot current time for created_at
        now = datetime.utcnow()

        # Make refresh() populate id + created_at
        def refresh_side_effect(instance):
            instance.id = TEST_IMAGE_ID
            instance.created_at = now

        # Configure DB-session mock
        mock_db_session.add.return_value = None
        mock_db_session.commit.return_value = None
        mock_db_session.refresh.side_effect = refresh_side_effect

        # Perform POST
        response = test_client.post(
            "/api/v1/assets/images/",
            files={"file": (TEST_FILENAME, create_test_image, "image/jpeg")},
            headers={"token": token},
        )

        assert response.status_code == 201, response.text
        body = response.json()
        assert body["id"] == TEST_IMAGE_ID
        assert body["small_url"] == TEST_IMAGE_URL
        assert body["medium_url"] == TEST_IMAGE_URL
        assert body["large_url"] == TEST_IMAGE_URL
        assert "created_at" in body and isinstance(body["created_at"], str)

@pytest.mark.asyncio
async def test_create_image_invalid_extension(test_client, mock_db_session, mock_admin_user, create_test_image):
    # Use disallowed extension
    token = Encryption.generate_token({"user_id": 1, "role": "admin"})
    response = test_client.post(
        "/api/v1/assets/images/",
        files={"file": ("bad.txt", create_test_image, "image/jpeg")},
        headers={"token": token},
    )
    assert response.status_code == 400
    assert "extension not allowed" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_create_image_invalid_file_type(test_client, mock_db_session, mock_admin_user):
    # Allowed extension but wrong content_type
    token = Encryption.generate_token({"user_id": 1, "role": "admin"})
    bad = BytesIO(b"not an image")
    response = test_client.post(
        "/api/v1/assets/images/",
        files={"file": ("invalid.jpg", bad, "text/plain")},
        headers={"token": token},
    )
    assert response.status_code == 400
    assert "file must be an image" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_get_image_success(test_client, mock_db_session):
    # Prepare a mock image record
    now = datetime.utcnow()
    mock_image = ImageModel(
        id=TEST_IMAGE_ID,
        small_url=TEST_IMAGE_URL,
        medium_url=TEST_IMAGE_URL,
        large_url=TEST_IMAGE_URL,
        created_at=now
    )
    mock_db_session.get.return_value = mock_image

    response = test_client.get(f"/api/v1/assets/images/{TEST_IMAGE_ID}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == TEST_IMAGE_ID
    assert body["small_url"] == TEST_IMAGE_URL
    assert body["medium_url"] == TEST_IMAGE_URL
    assert body["large_url"] == TEST_IMAGE_URL
    assert "created_at" in body and isinstance(body["created_at"], str)

@pytest.mark.asyncio
async def test_get_image_not_found(test_client, mock_db_session):
    mock_db_session.get.return_value = None

    response = test_client.get("/api/v1/assets/images/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Image not found"

@pytest.mark.asyncio
async def test_delete_image_success(test_client, mock_db_session, mock_admin_user):
    # Prepare a mock image record
    now = datetime.utcnow()
    mock_image = ImageModel(
        id=TEST_IMAGE_ID,
        small_url=TEST_IMAGE_URL,
        medium_url=TEST_IMAGE_URL,
        large_url=TEST_IMAGE_URL,
        created_at=now
    )
    mock_db_session.get.return_value = mock_image

    with patch("routers.images.views.S3") as mock_s3:
        mock_s3.delete_object.return_value = None
        response = test_client.delete(
            f"/api/v1/assets/images/{TEST_IMAGE_ID}",
            headers={"token": Encryption.generate_token({"user_id": 1, "role": "admin"})}
        )
        assert response.status_code == 204

@pytest.mark.asyncio
async def test_delete_image_not_found(test_client, mock_db_session, mock_admin_user):
    mock_db_session.get.return_value = None

    response = test_client.delete(
        f"/api/v1/assets/images/{TEST_IMAGE_ID}",
        headers={"token": Encryption.generate_token({"user_id": 1, "role": "admin"})}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Image not found"
