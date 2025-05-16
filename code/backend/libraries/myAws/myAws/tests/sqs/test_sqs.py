import pytest
from unittest.mock import patch, MagicMock
from myAws.sqs import SQS  # Adjust the import path as necessary
from myAws.config import Config
from myExceptions import aws as awsExceptions

# Fixtures for mocking boto3 resource
@pytest.fixture
def mock_boto3_resource():
    with patch('myAws.sqs.boto3.resource') as mock_resource:
        yield mock_resource

# Test Cases for SQS.post_to_queue

def test_post_to_queue_success(mock_boto3_resource):
    """
    Test that post_to_queue successfully posts a message to an SQS queue.
    """
    message = 'Test Message'
    queue_name = 'test-queue'
    mock_response = {
        'MessageId': '12345',
        'MD5OfMessageBody': 'abcde12345'
    }

    # Mock the SQS resource and queue
    mock_sqs_resource = MagicMock()
    mock_queue = MagicMock()
    mock_boto3_resource.return_value = mock_sqs_resource
    mock_sqs_resource.get_queue_by_name.return_value = mock_queue
    mock_queue.send_message.return_value = mock_response

    # Call the post_to_queue method
    response = SQS.post_to_queue(message, queue_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('sqs', region_name=Config.AWS_REGION)
    mock_sqs_resource.get_queue_by_name.assert_called_once_with(QueueName=queue_name)
    mock_queue.send_message.assert_called_once_with(MessageBody=message)
    assert response == mock_response

def test_post_to_queue_queue_not_found(mock_boto3_resource):
    """
    Test that post_to_queue raises SQSServiceError when the specified queue is not found.
    """
    message = 'Test Message'
    queue_name = 'nonexistent-queue'

    # Mock the SQS resource and get_queue_by_name to raise an exception
    mock_sqs_resource = MagicMock()
    mock_boto3_resource.return_value = mock_sqs_resource
    mock_sqs_resource.get_queue_by_name.side_effect = Exception("Queue does not exist")

    # Call the post_to_queue method and expect an exception
    with pytest.raises(awsExceptions.SQSServiceError) as exc_info:
        SQS.post_to_queue(message, queue_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('sqs', region_name=Config.AWS_REGION)
    mock_sqs_resource.get_queue_by_name.assert_called_once_with(QueueName=queue_name)
    mock_sqs_resource.get_queue_by_name.assert_called_once()
    mock_sqs_resource.get_queue_by_name.side_effect = Exception("Queue does not exist")
    assert f"Error in aws.sqs: Error uploading message: {message} to sqs queue: {queue_name}Queue does not exist" in str(exc_info.value)

def test_post_to_queue_send_message_failure(mock_boto3_resource):
    """
    Test that post_to_queue raises SQSServiceError when send_message fails.
    """
    message = 'Test Message'
    queue_name = 'test-queue'

    # Mock the SQS resource and queue
    mock_sqs_resource = MagicMock()
    mock_queue = MagicMock()
    mock_boto3_resource.return_value = mock_sqs_resource
    mock_sqs_resource.get_queue_by_name.return_value = mock_queue
    mock_queue.send_message.side_effect = Exception("Failed to send message")

    # Call the post_to_queue method and expect an exception
    with pytest.raises(awsExceptions.SQSServiceError) as exc_info:
        SQS.post_to_queue(message, queue_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('sqs', region_name=Config.AWS_REGION)
    mock_sqs_resource.get_queue_by_name.assert_called_once_with(QueueName=queue_name)
    mock_queue.send_message.assert_called_once_with(MessageBody=message)
    assert f"Error in aws.sqs: Error uploading message: {message} to sqs queue: {queue_name}Failed to send message" in str(exc_info.value)

def test_post_to_queue_general_exception(mock_boto3_resource):
    """
    Test that post_to_queue raises SQSServiceError for any unexpected exceptions.
    """
    message = 'Test Message'
    queue_name = 'test-queue'

    # Mock the SQS resource and queue to raise a general exception
    mock_sqs_resource = MagicMock()
    mock_queue = MagicMock()
    mock_boto3_resource.return_value = mock_sqs_resource
    mock_sqs_resource.get_queue_by_name.return_value = mock_queue
    mock_queue.send_message.side_effect = Exception("Unexpected error")

    # Call the post_to_queue method and expect an exception
    with pytest.raises(awsExceptions.SQSServiceError) as exc_info:
        SQS.post_to_queue(message, queue_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('sqs', region_name=Config.AWS_REGION)
    mock_sqs_resource.get_queue_by_name.assert_called_once_with(QueueName=queue_name)
    mock_queue.send_message.assert_called_once_with(MessageBody=message)
    assert f"Error in aws.sqs: Error uploading message: {message} to sqs queue: {queue_name}Unexpected error" in str(exc_info.value)

def test_post_to_queue_empty_message(mock_boto3_resource):
    """
    Test that post_to_queue successfully posts an empty message to an SQS queue.
    (Assuming that empty messages are allowed)
    """
    message = ''
    queue_name = 'test-queue'
    mock_response = {
        'MessageId': '12345',
        'MD5OfMessageBody': 'abcde12345'
    }

    # Mock the SQS resource and queue
    mock_sqs_resource = MagicMock()
    mock_queue = MagicMock()
    mock_boto3_resource.return_value = mock_sqs_resource
    mock_sqs_resource.get_queue_by_name.return_value = mock_queue
    mock_queue.send_message.return_value = mock_response

    # Call the post_to_queue method
    response = SQS.post_to_queue(message, queue_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('sqs', region_name=Config.AWS_REGION)
    mock_sqs_resource.get_queue_by_name.assert_called_once_with(QueueName=queue_name)
    mock_queue.send_message.assert_called_once_with(MessageBody=message)
    assert response == mock_response

def test_post_to_queue_invalid_queue_name(mock_boto3_resource):
    """
    Test that post_to_queue raises SQSServiceError when the queue name is invalid.
    """
    message = 'Test Message'
    queue_name = 'invalid-queue-name!@#'

    # Mock the SQS resource and get_queue_by_name to raise an exception
    mock_sqs_resource = MagicMock()
    mock_boto3_resource.return_value = mock_sqs_resource
    mock_sqs_resource.get_queue_by_name.side_effect = Exception("Invalid queue name")

    # Call the post_to_queue method and expect an exception
    with pytest.raises(awsExceptions.SQSServiceError) as exc_info:
        SQS.post_to_queue(message, queue_name)

    # Assertions
    mock_boto3_resource.assert_called_once_with('sqs', region_name=Config.AWS_REGION)
    mock_sqs_resource.get_queue_by_name.assert_called_once_with(QueueName=queue_name)
    assert f"Error in aws.sqs: Error uploading message: {message} to sqs queue: {queue_name}Invalid queue name" in str(exc_info.value)
