import os
import boto3
import blossom_exceptions
from .config import Config


class S3:
    @staticmethod
    def get_s3_client():
        return boto3.client('s3')

    @classmethod
    def upload_file(cls, bucket_name: str, object_name: str, file_path: str) -> None:
        """
        Uploads a file to an S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket.
            object_name (str): The name of the object in the S3 bucket.
            file_path (str): The local file path of the file to be uploaded.

        Raises:
            S3Exception: If an error occurs during the upload process.

        Returns:
            None
        """
        # check if file exists
        if not os.path.exists(file_path): raise blossom_exceptions.FileNotFoundError(f"File {file_path} not found.")
        try:
            client = cls.get_s3_client()
            client.upload_file(file_path, bucket_name, object_name)

            print(f'File {file_path} uploaded to bucket {bucket_name} as {object_name}.')
        except Exception as e:
            raise blossom_exceptions.S3ServiceError(f"Error in aws.s3: Error uploading file: {file_path} to bucket: {bucket_name}" + str(e))

    @classmethod
    def download_file(cls, bucket_name: str, object_name: str, file_path: str) -> None:
        """
        Downloads a file from an S3 bucket to a local file path.

        Args:
            bucket_name (str): The name of the S3 bucket.
            object_name (str): The name of the object/file in the S3 bucket.
            file_path (str): The local file path where the downloaded file will be saved.

        Raises:
            S3Exception: If an error occurs during the download process.

        Returns:
            None
        """
        # check if file is not already downloaded
        if os.path.exists(file_path): raise blossom_exceptions.FileAlreadyExistsError(f"File {file_path} already exists.")
        try:
            client = cls.get_s3_client()
            client.download_file(bucket_name, object_name, file_path)

            print(f'File {object_name} downloaded from bucket {bucket_name} to {file_path}.')
        except Exception as e:
            raise blossom_exceptions.S3ServiceError(f"Error in aws.s3: Error downloading file: {object_name} from bucket: {bucket_name}" + str(e))

    @staticmethod
    def generate_public_url(bucket_name: str, object_name: str) -> str:
        """
        Generate a public URL for an object in an S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket.
            object_name (str): The name of the object in the bucket.

        Returns:
            str: The public URL for the object.

        """
        return f"https://{bucket_name}.s3.{Config.AWS_REGION}.amazonaws.com/{object_name}"
