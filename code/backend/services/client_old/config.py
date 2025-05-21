import os
from myAws import SecretsManager
import json

class Config:
    JWT_SECRET_KEY = SecretsManager.get_secret("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"

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
