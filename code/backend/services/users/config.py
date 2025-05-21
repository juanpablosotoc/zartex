import logging
import sys

class Config:
    # Logging
    DEBUG_LOGS = True
    
# Configure logging to output to stdout
# Set log level based on Config.DEBUG_LOGS:
# - If DEBUG_LOGS is True, set level to DEBUG for detailed logs
# - If DEBUG_LOGS is False, set level to INFO for standard logs
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if Config.DEBUG_LOGS else logging.INFO)
logger = logging.getLogger(__name__)
