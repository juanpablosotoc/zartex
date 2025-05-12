import boto3
import myExceptions


class SQS:
    @staticmethod
    def post_to_queue(message, queueName):
        """
        Uploads a message to an SQS queue.

        Args:
            message (str): The message to be uploaded.
            queueName (str): The name of the SQS queue.

        Returns:
            dict: The response from the SQS queue.

        Raises:
            SQSException: If there is an error while uploading the message.
        """
        try:
            sqs = boto3.resource('sqs')
            queue = sqs.get_queue_by_name(QueueName=queueName)
            response = queue.send_message(MessageBody=message)
            return response
        except Exception as e:
            raise myExceptions.SQSServiceError(f'Error in aws.sqs: Error uploading message: {message} to sqs queue: {queueName}' + str(e))
