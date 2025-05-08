import pytest
from unittest.mock import patch, MagicMock
from aws import S3
import blossom_exceptions
from aws.config import Config 


# Fixtures for mocking boto3 client and Config.AWS_REGION
@pytest.fixture
def mock_boto3_client():
    with patch('aws.s3.boto3.client') as mock_client:
        yield mock_client

@pytest.fixture
def mock_config_aws_region():
    with patch.object(Config, 'AWS_REGION', 'us-west-2'):
        yield

# Tests for upload_file
def test_upload_file_success(mock_boto3_client, mock_config_aws_region):
    bucket_name = 'test-bucket'
    object_name = 'test-object'
    file_path = '/path/to/test-file.txt'

    # Mock os.path.exists to return True
    with patch('aws.s3.os.path.exists', return_value=True):
        # Mock the S3 client and its upload_file method
        mock_client_instance = MagicMock()
        mock_boto3_client.return_value = mock_client_instance

        # Call the upload_file method
        S3.upload_file(bucket_name, object_name, file_path)

        # Assert that upload_file was called with correct parameters
        mock_client_instance.upload_file.assert_called_once_with(file_path, bucket_name, object_name)

def test_upload_file_file_not_found(mock_boto3_client, mock_config_aws_region):
    bucket_name = 'test-bucket'
    object_name = 'test-object'
    file_path = '/path/to/nonexistent-file.txt'

    # Mock os.path.exists to return False
    with patch('aws.s3.os.path.exists', return_value=False):
        with pytest.raises(blossom_exceptions.FileNotFoundError) as exc_info:
            S3.upload_file(bucket_name, object_name, file_path)
        
        assert f"File {file_path} not found." in str(exc_info.value)
        mock_boto3_client.assert_not_called()

def test_upload_file_boto3_exception(mock_boto3_client, mock_config_aws_region):
    bucket_name = 'test-bucket'
    object_name = 'test-object'
    file_path = '/path/to/test-file.txt'

    # Mock os.path.exists to return True
    with patch('aws.s3.os.path.exists', return_value=True):
        # Mock the S3 client and its upload_file method to raise an exception
        mock_client_instance = MagicMock()
        mock_client_instance.upload_file.side_effect = Exception("Upload failed")
        mock_boto3_client.return_value = mock_client_instance

        with pytest.raises(blossom_exceptions.S3ServiceError) as exc_info:
            S3.upload_file(bucket_name, object_name, file_path)
        
        assert f"Error in aws.s3: Error uploading file: {file_path} to bucket: {bucket_name}Upload failed" in str(exc_info.value)

# Tests for download_file
def test_download_file_success(mock_boto3_client, mock_config_aws_region):
    bucket_name = 'test-bucket'
    object_name = 'test-object'
    file_path = '/path/to/downloaded-file.txt'

    # Mock os.path.exists to return False
    with patch('aws.s3.os.path.exists', return_value=False):
        # Mock the S3 client and its download_file method
        mock_client_instance = MagicMock()
        mock_boto3_client.return_value = mock_client_instance

        # Call the download_file method
        S3.download_file(bucket_name, object_name, file_path)

        # Assert that download_file was called with correct parameters
        mock_client_instance.download_file.assert_called_once_with(bucket_name, object_name, file_path)

def test_download_file_already_exists(mock_boto3_client, mock_config_aws_region):
    bucket_name = 'test-bucket'
    object_name = 'test-object'
    file_path = '/path/to/existing-file.txt'

    # Mock os.path.exists to return True
    with patch('aws.s3.os.path.exists', return_value=True):
        with pytest.raises(blossom_exceptions.FileAlreadyExistsError) as exc_info:
            S3.download_file(bucket_name, object_name, file_path)
        
        assert f"File {file_path} already exists." in str(exc_info.value)
        mock_boto3_client.assert_not_called()

def test_download_file_boto3_exception(mock_boto3_client, mock_config_aws_region):
    bucket_name = 'test-bucket'
    object_name = 'test-object'
    file_path = '/path/to/downloaded-file.txt'

    # Mock os.path.exists to return False
    with patch('aws.s3.os.path.exists', return_value=False):
        # Mock the S3 client and its download_file method to raise an exception
        mock_client_instance = MagicMock()
        mock_client_instance.download_file.side_effect = Exception("Download failed")
        mock_boto3_client.return_value = mock_client_instance

        with pytest.raises(blossom_exceptions.S3ServiceError) as exc_info:
            S3.download_file(bucket_name, object_name, file_path)
        
        assert f"Error in aws.s3: Error downloading file: {object_name} from bucket: {bucket_name}Download failed" in str(exc_info.value)

# Tests for generate_public_url
def test_generate_public_url(mock_config_aws_region):
    bucket_name = 'test-bucket'
    object_name = 'test-object'
    expected_url = f"https://{bucket_name}.s3.us-west-2.amazonaws.com/{object_name}"

    url = S3.generate_public_url(bucket_name, object_name)

    assert url == expected_url
