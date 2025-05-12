class AWSError(Exception):
    """Base class for AWS service-related errors."""
    error_code = 'aws_error'
    message = "An AWS service error occurred."


class S3ServiceError(AWSError):
    """Raised when an S3 service request fails."""
    error_code = 's3_service_error'
    message = "Failed to communicate with S3 service."


class DynamoDBServiceError(AWSError):
    """Raised when a DynamoDB service request fails."""
    error_code = 'dynamodb_service_error'
    message = "Failed to communicate with DynamoDB service."


class SecretsManagerServiceError(AWSError):
    """Raised when a Secrets Manager service request fails."""
    error_code = 'secrets_manager_service_error'
    message = "Failed to communicate with Secrets Manager service."


class SQSServiceError(AWSError):
    """Raised when an SQS service request fails."""
    error_code = 'sqs_service_error'
    message = "Failed to communicate with SQS service."
