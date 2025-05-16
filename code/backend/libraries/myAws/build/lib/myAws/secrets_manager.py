import boto3
from myExceptions import aws as awsExceptions
from .config import Config

class SecretsManager:
    @staticmethod
    def get_secret(secret_name: str) -> str:
        """
        Retrieves the value of a secret from AWS Secrets Manager.

        Args:
            secret_name (str): The name or ARN of the secret.

        Returns:
            str | dict: The secret value, either as a string or a dictionary.

        Raises:
            SecretsManagerException: If there is an error retrieving the secret.
        """
        try:
            session = boto3.Session(region_name=Config.AWS_REGION)
            # Assume the role
            client = session.client(service_name='secretsmanager')
            # Retrieve the secret value
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )

            # Extract the secret value
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = get_secret_value_response['SecretBinary']

            return secret

        except Exception as e:
            raise awsExceptions.SecretsManagerServiceError(f'Error in aws.secrets_manager: Error retrieving secret: {secret_name} ' + str(e))
        