import pytest
import jwt
from myEncryption import Encryption
from config import Config


@pytest.fixture
def sample_password():
    return "test_password123"


@pytest.fixture
def sample_data():
    return {"user_id": 1, "role": "admin"}


def test_hash_password(sample_password):
    # Test password hashing
    hashed = Encryption.hash_password(sample_password)
    
    # Check that the hash is different from the original password
    assert hashed != sample_password
    
    # Check that the hash is a string
    assert isinstance(hashed, str)
    
    # Check that the hash starts with the bcrypt identifier
    assert hashed.startswith('$2b$')


def test_verify_password_correct(sample_password):
    # Test password verification with correct password
    hashed = Encryption.hash_password(sample_password)
    assert Encryption.verify_password(sample_password, hashed)


def test_verify_password_incorrect(sample_password):
    # Test password verification with incorrect password
    hashed = Encryption.hash_password(sample_password)
    assert not Encryption.verify_password("wrong_password", hashed)


def test_generate_token(sample_data):
    # Test token generation
    token = Encryption.generate_token(sample_data)
    
    # Check that the token is a string
    assert isinstance(token, str)
    
    # Check that the token can be decoded
    decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
    assert decoded == sample_data


def test_verify_token_valid(sample_data):
    # Test token verification with valid token
    token = Encryption.generate_token(sample_data)
    decoded = Encryption.verify_token(token)
    assert decoded == sample_data


def test_verify_token_invalid():
    # Test token verification with invalid token
    with pytest.raises(jwt.exceptions.InvalidTokenError):
        Encryption.verify_token("invalid_token")


def test_verify_token_tampered(sample_data):
    # Test token verification with tampered token
    token = Encryption.generate_token(sample_data)
    tampered_token = token[:-1] + ('1' if token[-1] == '0' else '0')
    
    with pytest.raises(jwt.exceptions.InvalidTokenError):
        Encryption.verify_token(tampered_token)


def test_verify_token_expired(sample_data):
    # Test token verification with expired token
    import time
    data = sample_data.copy()
    data['exp'] = int(time.time()) - 1  # Set expiration to 1 second ago
    
    token = jwt.encode(data, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    
    with pytest.raises(jwt.exceptions.ExpiredSignatureError):
        Encryption.verify_token(token) 
        