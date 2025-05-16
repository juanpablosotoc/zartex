import pytest
from unittest.mock import patch, MagicMock
from myAws.dynamodb import DynamoDB
from myExceptions import aws as awsExceptions


# Fixtures for mocking boto3 resource and Config.AWS_REGION
@pytest.fixture
def mock_boto3_resource():
    with patch('myAws.dynamodb.boto3.resource') as mock_resource:
        yield mock_resource

@pytest.fixture
def mock_config_aws_region():
    with patch('myAws.dynamodb.Config.AWS_REGION', 'mx-central-1'):
        yield

# Test Cases for DynamoDB.get_table

def test_get_table_success(mock_boto3_resource, mock_config_aws_region):
    """
    Test that get_table successfully retrieves a DynamoDB table.
    """
    table_name = 'test-table'
    mock_table = MagicMock()

    # Mock the DynamoDB resource and Table
    mock_dynamodb_resource = MagicMock()
    mock_boto3_resource.return_value = mock_dynamodb_resource
    mock_dynamodb_resource.Table.return_value = mock_table

    # Call the get_table method
    table = DynamoDB.get_table(table_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('dynamodb', region_name='mx-central-1')
    mock_dynamodb_resource.Table.assert_called_once_with(table_name)
    assert table == mock_table

def test_get_table_exception(mock_boto3_resource, mock_config_aws_region):
    """
    Test that get_table raises DynamoDBServiceError when an exception occurs.
    """
    table_name = 'test-table-error'

    # Mock the DynamoDB resource to raise an exception when Table is called
    mock_dynamodb_resource = MagicMock()
    mock_boto3_resource.return_value = mock_dynamodb_resource
    mock_dynamodb_resource.Table.side_effect = Exception("Failed to retrieve table")

    # Call the get_table method and expect an exception
    with pytest.raises(awsExceptions.DynamoDBServiceError) as exc_info:
        DynamoDB.get_table(table_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('dynamodb', region_name='mx-central-1')
    mock_dynamodb_resource.Table.assert_called_once_with(table_name)
    assert f"Error in aws.dynamodb: Error retrieving table: {table_name}. Failed to retrieve table" in str(exc_info.value)

# Test Cases for DynamoDB.put_item

def test_put_item_success(mock_boto3_resource, mock_config_aws_region):
    """
    Test that put_item successfully puts an item into the DynamoDB table.
    """
    table_name = 'test-table'
    item = {'id': '123', 'name': 'Test Item'}
    mock_table = MagicMock()

    # Mock the DynamoDB resource and Table
    mock_dynamodb_resource = MagicMock()
    mock_boto3_resource.return_value = mock_dynamodb_resource
    mock_dynamodb_resource.Table.return_value = mock_table

    # Call the put_item method
    DynamoDB.put_item(item, table_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('dynamodb', region_name='mx-central-1')
    mock_dynamodb_resource.Table.assert_called_once_with(table_name)
    mock_table.put_item.assert_called_once_with(Item=item)

def test_put_item_exception_put_item(mock_boto3_resource, mock_config_aws_region):
    """
    Test that put_item raises DynamoDBServiceError when put_item raises an exception.
    """
    table_name = 'test-table-error'
    item = {'id': '123', 'name': 'Test Item'}

    # Mock the DynamoDB resource and Table
    mock_dynamodb_resource = MagicMock()
    mock_table = MagicMock()
    mock_boto3_resource.return_value = mock_dynamodb_resource
    mock_dynamodb_resource.Table.return_value = mock_table

    # Configure put_item to raise an exception
    mock_table.put_item.side_effect = Exception("Failed to put item")

    # Call the put_item method and expect an exception
    with pytest.raises(awsExceptions.DynamoDBServiceError) as exc_info:
        DynamoDB.put_item(item, table_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('dynamodb', region_name='mx-central-1')
    mock_dynamodb_resource.Table.assert_called_once_with(table_name)
    mock_table.put_item.assert_called_once_with(Item=item)
    assert f"Error in aws.dynamodb: Error putting item: {item} into table: {table_name}. Failed to put item" in str(exc_info.value)

# Test Cases for DynamoDB.get_item

def test_get_item_success_item_exists(mock_boto3_resource, mock_config_aws_region):
    """
    Test that get_item successfully retrieves an existing item from the DynamoDB table.
    """
    table_name = 'test-table'
    key = {'id': '123'}
    expected_item = {'id': '123', 'name': 'Test Item'}
    mock_table = MagicMock()

    # Mock the DynamoDB resource and Table
    mock_dynamodb_resource = MagicMock()
    mock_boto3_resource.return_value = mock_dynamodb_resource
    mock_dynamodb_resource.Table.return_value = mock_table

    # Mock the get_item response with an existing item
    mock_table.get_item.return_value = {
        'Item': expected_item
    }

    # Call the get_item method
    item = DynamoDB.get_item(key, table_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('dynamodb', region_name='mx-central-1')
    mock_dynamodb_resource.Table.assert_called_once_with(table_name)
    mock_table.get_item.assert_called_once_with(Key=key)
    assert item == expected_item

def test_get_item_success_item_does_not_exist(mock_boto3_resource, mock_config_aws_region):
    """
    Test that get_item returns None when the item does not exist in the DynamoDB table.
    """
    table_name = 'test-table'
    key = {'id': '999'}
    mock_table = MagicMock()

    # Mock the DynamoDB resource and Table
    mock_dynamodb_resource = MagicMock()
    mock_boto3_resource.return_value = mock_dynamodb_resource
    mock_dynamodb_resource.Table.return_value = mock_table

    # Mock the get_item response without 'Item'
    mock_table.get_item.return_value = {}

    # Call the get_item method
    item = DynamoDB.get_item(key, table_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('dynamodb', region_name='mx-central-1')
    mock_dynamodb_resource.Table.assert_called_once_with(table_name)
    mock_table.get_item.assert_called_once_with(Key=key)
    assert item is None

def test_get_item_exception_get_item(mock_boto3_resource, mock_config_aws_region):
    """
    Test that get_item raises DynamoDBServiceError when table.get_item raises an exception.
    """
    table_name = 'test-table-error'
    key = {'id': '123'}

    # Mock the DynamoDB resource and Table
    mock_dynamodb_resource = MagicMock()
    mock_table = MagicMock()
    mock_boto3_resource.return_value = mock_dynamodb_resource
    mock_dynamodb_resource.Table.return_value = mock_table

    # Configure get_item to raise an exception
    mock_table.get_item.side_effect = Exception("Failed to get item")

    # Call the get_item method and expect an exception
    with pytest.raises(awsExceptions.DynamoDBServiceError) as exc_info:
        DynamoDB.get_item(key, table_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('dynamodb', region_name='mx-central-1')
    mock_dynamodb_resource.Table.assert_called_once_with(table_name)
    mock_table.get_item.assert_called_once_with(Key=key)
    assert f"Error in aws.dynamodb: Error getting item with key: {key} from table: {table_name}. Failed to get item" in str(exc_info.value)

# Additional Edge Case Tests

def test_put_item_invalid_item(mock_boto3_resource, mock_config_aws_region):
    """
    Test that put_item raises DynamoDBServiceError when an invalid item is provided.
    """
    table_name = 'test-table'
    invalid_item = {'id': None, 'name': 'Test Item'}  # Assuming 'id' cannot be None

    # Mock the DynamoDB resource and Table
    mock_dynamodb_resource = MagicMock()
    mock_table = MagicMock()
    mock_boto3_resource.return_value = mock_dynamodb_resource
    mock_dynamodb_resource.Table.return_value = mock_table

    # Configure put_item to raise a specific exception (e.g., ValidationException)
    mock_table.put_item.side_effect = Exception("ValidationException: Item has null primary key")

    # Call the put_item method and expect an exception
    with pytest.raises(awsExceptions.DynamoDBServiceError) as exc_info:
        DynamoDB.put_item(invalid_item, table_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('dynamodb', region_name='mx-central-1')
    mock_dynamodb_resource.Table.assert_called_once_with(table_name)
    mock_table.put_item.assert_called_once_with(Item=invalid_item)
    assert f"Error in aws.dynamodb: Error putting item: {invalid_item} into table: {table_name}. ValidationException: Item has null primary key" in str(exc_info.value)

def test_get_item_invalid_key(mock_boto3_resource, mock_config_aws_region):
    """
    Test that get_item raises DynamoDBServiceError when an invalid key is provided.
    """
    table_name = 'test-table'
    invalid_key = {'id': None}  # Assuming 'id' cannot be None

    # Mock the DynamoDB resource and Table
    mock_dynamodb_resource = MagicMock()
    mock_table = MagicMock()
    mock_boto3_resource.return_value = mock_dynamodb_resource
    mock_dynamodb_resource.Table.return_value = mock_table

    # Configure get_item to raise a specific exception (e.g., ValidationException)
    mock_table.get_item.side_effect = Exception("ValidationException: Key has null attribute")

    # Call the get_item method and expect an exception
    with pytest.raises(awsExceptions.DynamoDBServiceError) as exc_info:
        DynamoDB.get_item(invalid_key, table_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('dynamodb', region_name='mx-central-1')
    mock_dynamodb_resource.Table.assert_called_once_with(table_name)
    mock_table.get_item.assert_called_once_with(Key=invalid_key)
    assert f"Error in aws.dynamodb: Error getting item with key: {invalid_key} from table: {table_name}. ValidationException: Key has null attribute" in str(exc_info.value)
