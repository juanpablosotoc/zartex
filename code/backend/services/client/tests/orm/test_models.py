import pytest
from orm.models import Client, Image
import bcrypt


@pytest.fixture
def sample_client_data():
    """Sample data for creating a test client."""
    password = "testpassword123"
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return {
        "email": "test@example.com",
        "password_hash": password_hash,
        "first_name": "Test",
        "last_name": "User",
        "is_admin": False
    }


@pytest.fixture
def sample_image_data():
    """Sample data for creating a test image."""
    return {
        "small_url": "https://example.com/small.jpg",
        "medium_url": "https://example.com/medium.jpg",
        "large_url": "https://example.com/large.jpg"
    }


@pytest.mark.asyncio
async def test_create_client(db_session, sample_client_data):
    """Test creating a client."""
    client = Client(**sample_client_data)
    db_session.add(client)
    await db_session.commit()
    await db_session.refresh(client)
    
    assert client.id is not None
    assert client.email == sample_client_data["email"]
    assert client.first_name == sample_client_data["first_name"]
    assert client.last_name == sample_client_data["last_name"]


@pytest.mark.asyncio
async def test_create_image(db_session, sample_image_data):
    """Test creating an image."""
    image = Image(**sample_image_data)
    db_session.add(image)
    await db_session.commit()
    await db_session.refresh(image)
    
    assert image.id is not None
    assert image.small_url == sample_image_data["small_url"]
    assert image.medium_url == sample_image_data["medium_url"]
    assert image.large_url == sample_image_data["large_url"]


@pytest.mark.asyncio
async def test_client_password_hashing(db_session, sample_client_data):
    """Test that client passwords are properly hashed."""
    client = Client(**sample_client_data)
    db_session.add(client)
    await db_session.commit()
    await db_session.refresh(client)
    
    # Password should be hashed
    assert client.password_hash != "testpassword123"
    assert client.password_hash.startswith("$2b$")  # bcrypt hash format


@pytest.mark.asyncio
async def test_client_email_uniqueness(db_session, sample_client_data):
    """Test that client emails must be unique."""
    # Create first client
    client1 = Client(**sample_client_data)
    db_session.add(client1)
    await db_session.commit()
    
    # Try to create second client with same email
    client2 = Client(**sample_client_data)
    db_session.add(client2)
    with pytest.raises(Exception):  # SQLAlchemy will raise an integrity error
        await db_session.commit()


@pytest.mark.asyncio
async def test_client_admin_default(db_session, sample_client_data):
    """Test that is_admin defaults to False."""
    # Remove is_admin from data
    data = sample_client_data.copy()
    del data["is_admin"]
    
    client = Client(**data)
    db_session.add(client)
    await db_session.commit()
    await db_session.refresh(client)
    
    assert client.is_admin is False


@pytest.mark.asyncio
async def test_image_urls_required(db_session):
    """Test that image URLs are required."""
    # Try to create image without URLs
    image = Image()
    db_session.add(image)
    with pytest.raises(Exception):  # SQLAlchemy will raise an integrity error
        await db_session.commit() 
        