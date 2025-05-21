from .config import Config
import bcrypt
import jwt


class Encryption:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    
    @staticmethod
    def generate_token(data: dict) -> str:
        """
        Generate a jwt token for the given payload
        """
        return jwt.encode(data, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verify the token and return the decoded payload
        
        Raises:
            jwt.exceptions.InvalidTokenError: If the token is invalid
        """
        return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])

