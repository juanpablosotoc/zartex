from myAws import SecretsManager


class Config:
    JWT_SECRET_KEY = SecretsManager.get_secret("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
