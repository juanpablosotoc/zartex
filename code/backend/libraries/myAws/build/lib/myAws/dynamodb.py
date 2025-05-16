import boto3
from myExceptions import aws as awsExceptions
from .config import Config
import logging

logger = logging.getLogger(__name__)

class DynamoDB:
    @staticmethod
    def get_table(table_name: str):
        """
        Retrieves a DynamoDB table object based on the provided table name.

        Args:
            table_name (str): The name of the DynamoDB table.

        Returns:
            table (boto3.resources.factory.dynamodb.Table): The DynamoDB table object.

        Raises:
            DynamoDBServiceError: If there is an error retrieving the table or if the credentials are not available.
        """
        try:
            # Create a DynamoDB resource
            dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)    
            # Specify the table you want to interact with
            table = dynamodb.Table(table_name)
            return table
        except Exception as e:
            error_message = f'Error in aws.dynamodb: Error retrieving table: {table_name}. {str(e)}'
            logger.error(f"DynamoDBServiceError | Message: {error_message} | Status Code: 502 | Error Code: dynamodb_service_error")
            raise awsExceptions.DynamoDBServiceError(error_message)
    
    @classmethod
    def put_item(cls, item: dict, table_name: str) -> None:
        """
        Puts an item into the specified DynamoDB table.

        Args:
            item (dict): The item to be put into the table.
            table_name (str): The name of the table.

        Raises:
            DynamoDBServiceError: If an error occurs while putting the item.

        Returns:
            None
        """
        try:
            table = cls.get_table(table_name)
            table.put_item(Item=item)
        except awsExceptions.DynamoDBServiceError as e:
            # Re-raise with additional context
            error_message = f'Error in aws.dynamodb: Error putting item: {item} into table: {table_name}. {str(e)}'
            logger.error(f"DynamoDBServiceError | Message: {error_message} | Status Code: 502 | Error Code: dynamodb_service_error")
            raise awsExceptions.DynamoDBServiceError(error_message) from e
        except Exception as e:
            # Wrap any other exceptions
            error_message = f'Error in aws.dynamodb: Error putting item: {item} into table: {table_name}. {str(e)}'
            logger.error(f"DynamoDBServiceError | Message: {error_message} | Status Code: 502 | Error Code: dynamodb_service_error")
            raise awsExceptions.DynamoDBServiceError(error_message) from e
                
    @classmethod
    def get_item(cls, key: dict, table_name: str) -> dict:
        """
        Retrieves an item from the specified DynamoDB table based on the provided key.

        Args:
            key (dict): The key used to retrieve the item.
            table_name (str): The name of the DynamoDB table.

        Returns:
            dict: The retrieved item, or None if the item does not exist.

        Raises:
            DynamoDBServiceError: If an error occurs while retrieving the item.
        """
        try:
            table = cls.get_table(table_name)
            response = table.get_item(Key=key)
            return response.get('Item', None)
        except awsExceptions.DynamoDBServiceError as e:
            # Re-raise with additional context
            error_message = f'Error in aws.dynamodb: Error getting item with key: {key} from table: {table_name}. {str(e)}'
            logger.error(f"DynamoDBServiceError | Message: {error_message} | Status Code: 502 | Error Code: dynamodb_service_error")
            raise awsExceptions.DynamoDBServiceError(error_message) from e
        except Exception as e:
            # Wrap any other exceptions
            error_message = f'Error in aws.dynamodb: Error getting item with key: {key} from table: {table_name}. {str(e)}'
            logger.error(f"DynamoDBServiceError | Message: {error_message} | Status Code: 502 | Error Code: dynamodb_service_error")
            raise awsExceptions.DynamoDBServiceError(error_message) from e
