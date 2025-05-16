import os
from myExceptions import boot as bootExceptions


class Config:
    AWS_REGION = os.getenv('AWS_REGION')
    if not AWS_REGION: raise bootExceptions.ConfigurationError('Error in aws package: AWS_REGION not set')
