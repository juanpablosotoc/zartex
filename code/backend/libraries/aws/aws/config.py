import os
import blossom_exceptions


class Config:
    AWS_REGION = os.getenv('AWS_REGION')
    if not AWS_REGION: raise blossom_exceptions.ConfigurationError('Error in aws package: AWS_REGION not set')
