# -*- coding: utf-8 -*-
import os
import json
import boto3
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]))


class BatchProcessingFailedException(Exception):
    """Raise for failed messages during processing in batch."""


class SQSService:
    """Simplify queue operations via AWS Simple Queue Service."""

    def __init__(self, region_name="eu-west-2"):
        """Initialize default region.

        :param region_name: the AWS region name, default eu-central-1
        """
        self.sqs = boto3.client("sqs", region_name=region_name)

    def send_message_to_fifo(self, message, queue_url):
        """Send a message to the FIFO SQS queue.

        :param message: Message payload - string
        :param queue_url: the AWS SQS queue URL
        :return: NotImplemented
        """
        try:
            self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=message["MessageBody"],
                DelaySeconds=message["DelaySeconds"],
                MessageAttributes=message["MessageAttributes"],
                MessageGroupId=message["MessageGroupId"],
                MessageDeduplicationId=message["Id"],
            )
            LOGGER.info(f"Message sent to queue {queue_url}")
        except ClientError:
            LOGGER.error(f"Failed to send message to queue {queue_url}")
            raise

    def send_message(self, message, queue_url):
        """Send a message to regular queue.

        :param message: message payload - string
        :param queue_url: the AWS SQS queue URL
        :return: NotImplemented
        """
        try:
            self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=message["MessageBody"],
                DelaySeconds=message.get("DelaySeconds", 0),
                MessageAttributes=message.get("MessageAttributes", {}),
            )
            LOGGER.info(f"Message sent to queue {queue_url}")
        except ClientError:
            LOGGER.error(f"Failed to send message to queue {queue_url}")
            raise

    @staticmethod
    def _retry_failed_messages(queue_url, response, messages, retry, retry_function):
        """Retry failed messages.

        :param queue_url:
        :param response:
        :param messages:
        :param retry:
        :param retry_function:
        :return:
        """
        failed = response.get("Failed")
        while failed and retry > 0:
            LOGGER.info(f"Retry {len(failed)} failed messages")
            failed_ids = [fail["Id"] for fail in failed]
            failed_messages = [message for message in messages if message["Id"] in failed_ids]
            response = retry_function(QueueUrl=queue_url, Entries=failed_messages)
            failed = response.get("Failed")
            retry -= 1
        if failed:
            LOGGER.error(f"Failed to process message batch {queue_url} due to {json.dumps(failed)}")
            raise BatchProcessingFailedException()

    def send_messages(self, messages, queue_url, retry=3):
        """Send 10 messages in batch to the SQS queue.

        :param messages: List of messages
        :param queue_url: the AWS SQS queue URL
        :param retry: number of times to retry
        :return: NotImplemented
        """
        try:
            chunk_size = 10
            for idx in range(0, len(messages), chunk_size):
                chunk = messages[idx : idx + chunk_size]
                response = self.sqs.send_message_batch(QueueUrl=queue_url, Entries=chunk)
                self._retry_failed_messages(queue_url, response, chunk, retry, self.sqs.send_message_batch)
            LOGGER.info(f"Sent {len(messages)} message to queue {queue_url}")
        except ClientError:
            LOGGER.error(f"Failed to send message batch to queue {queue_url}")
            raise

    def receive_messages(self, queue_url, **kwargs):
        """Receive a defined number of messages from queue.

        :param queue_url: The AWS SQS queue URL
        :param kwargs: dictionary of key/value pairs to pass to SQS client
        :return: messages list
        """
        try:
            num_of_messages = kwargs.get("max_number_of_messages", 1)
            messages = []

            while num_of_messages > 0:
                max_messages = min(num_of_messages, 10)
                response = self.sqs.receive_message(
                    QueueUrl=queue_url,
                    AttributeNames=[kwargs.get("attribute_names", "All")],
                    MaxNumberOfMessages=kwargs.get("max_messages", max_messages),
                    MessageAttributeNames=[kwargs.get("message_attribute_names", "All")],
                    WaitTimeSeconds=kwargs.get("wait_time", 3),
                )
                new_messages = response.get("Messages", [])
                if not new_messages:
                    LOGGER.info("No messages in queue")
                    return "No messages in queue"
                messages.extend(new_messages)
                num_of_messages -= max_messages
            LOGGER.info(f"Received {len(messages)} messages from queue {queue_url}")
            return messages
        except ClientError:
            LOGGER.error(f"Failed to receive messages from queue {queue_url}")
            raise

    def delete_message(self, queue_url, receipt_handle):
        """Delete a message from queue.

        :param queue_url: the AWS SQS queue URL
        :param receipt_handle: receipt_handle from sqs message
        :return: NotImplemented
        """
        try:
            self.sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
            LOGGER.debug("Removed message from queue")
        except ClientError:
            LOGGER.error(f"Failed to delete message from queue {queue_url}")
            raise

    def delete_messages(self, queue_url, messages, retry=3):
        """Delete multiple messages (10) from the SQS queue.

        :param queue_url: The AWS SQS queue URL
        :param messages: list of SQS messages
        :param retry: number of times to retry
        :return: NotImplemented
        """
        try:
            chunk_size = 10
            for i in range(0, len(messages), chunk_size):
                chunk = messages[i : i + chunk_size]
                entries = [{"Id": x["MessageId"], "ReceiptHandle": x["ReceiptHandle"]} for x in chunk]
                response = self.sqs.delete_message_batch(QueueUrl=queue_url, Entries=entries)
                self._retry_failed_messages(queue_url, response, chunk, retry, self.sqs.delete_message_batch)
            LOGGER.info(f"Deleted {len(messages)} message from queue {queue_url}")
        except ClientError:
            LOGGER.error(f"Failed to delete messages from queue {queue_url}")
            raise

    def get_queue_attr(self, queue_url, attribute_names):
        """Get SQS queue attributes.

        :param queue_url: the AWS SQS queue URL
        :param attribute_names: name of SQS queue attributes
        :return: attributes dict
        """
        try:
            response = self.sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=attribute_names)
            LOGGER.info(f"Got {attribute_names} attributes for queue {queue_url}")
            return response["Attributes"]
        except ClientError:
            LOGGER.error(f"Failed to get attributes for queue {queue_url}")
            raise

    def queue_has_messages(self, queue_name: str) -> int:
        """Check if a queue has messages.

        :param queue_name: The AWS SQS queue name
        :return: number of messages
        """
        attr = self.get_queue_attr(queue_name, ["ApproximateNumberOfMessages"])
        return int(attr["ApproximateNumberOfMessages"]) > 0

    def queue_has_messages_in_flight(self, queue_name: str) -> int:
        """Check if a queue has messages in flight (actually processing).

        :param queue_name: The AWS SQS queue name
        :return: number of messages
        """
        attr = self.get_queue_attr(queue_name, ["ApproximateNumberOfMessagesNotVisible"])
        return int(attr["ApproximateNumberOfMessagesNotVisible"]) > 0
