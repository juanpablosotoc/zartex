import os
from myAws import SecretsManager
import json

class Config:
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
