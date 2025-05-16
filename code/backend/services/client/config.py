import os
from myAws import SecretsManager
import json

class Config:
    JWT_SECRET_KEY = SecretsManager.get_secret("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"

    # Database
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_PORT = os.getenv("DATABASE_PORT")

    # Get db user and password from secret manager
    DATABASE_CREDENTIALS = json.loads(SecretsManager.get_secret(os.getenv("DATABASE_CREDENTIALS_SECRET_NAME")))
    DATABASE_USER = DATABASE_CREDENTIALS["username"]
    DATABASE_PASSWORD = DATABASE_CREDENTIALS["password"]

    DATABASE_URL = f"mysql+aiomysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    ECHO_SQL = True

    # Logging
    DEBUG_LOGS = True

    # Image 
    IMAGE_SIZES = {
        "small": (300, 300), # 300x300 in pixels
        "medium": (600, 600), # 600x600 in pixels
        "large": (1200, 1200) # 1200x1200 in pixels
    }

    S3_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    def gen_object_name(self, size_name: str, filename: str):
        return f"images/{size_name}/{filename}"
