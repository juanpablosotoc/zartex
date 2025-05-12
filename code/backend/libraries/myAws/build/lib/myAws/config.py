import os
import myExceptions


class Config:
    AWS_REGION = os.getenv('AWS_REGION')
    if not AWS_REGION: raise myExceptions.ConfigurationError('Error in aws package: AWS_REGION not set')
