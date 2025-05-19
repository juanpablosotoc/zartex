import os
import logging
import sys

class Config:
    # Constants
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic', '.heif'}
    MAX_IMAGE_DIMENSION = 5000 # pixels

    # Logging
    DEBUG_LOGS = True

    # Image 
    IMAGE_SIZES = {
        "small": (300, 300), # 300x300 in pixels
        "medium": (600, 600), # 600x600 in pixels
        "large": (1200, 1200) # 1200x1200 in pixels
    }

    S3_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    @staticmethod
    def gen_object_name(size_name: str, filename: str):
        return f"images/{size_name}/{filename}"
    
# Configure logging to output to stdout
# Set log level based on Config.DEBUG_LOGS:
# - If DEBUG_LOGS is True, set level to DEBUG for detailed logs
# - If DEBUG_LOGS is False, set level to INFO for standard logs
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if Config.DEBUG_LOGS else logging.INFO)
logger = logging.getLogger(__name__)
