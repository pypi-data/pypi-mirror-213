import logging
import boto3
from botocore.exceptions import ClientError
from cloudservices.config import cloud_config
from cloudservices.queueservice.queue import Queue


class SQS(Queue):
    """A SQS client for sending and receiving messages from a queue.

    Args:
        topic_name (str, optional): The name of the topic to subscribe to. Defaults to None.
        subscription_name (str, optional): The name of the subscription to use. Defaults to None.

    Returns:
        None : The SQS client is initialized.

    """

    def __init__(self, topic_name=None, subscription_name=None):

        if topic_name is None and subscription_name is None:
            raise ValueError(
                'Either topic_name or subscription_name must be provided.')
        try:
            sqs_resource = boto3.resource("sqs",  aws_access_key_id=cloud_config.aws_access_key_id,
                                          aws_secret_access_key=cloud_config.aws_secret_access_key, region_name=cloud_config.aws_region)

            if topic_name is not None:
                self.topic_name = topic_name
                self.publisher = sqs_resource.get_queue_by_name(
                    QueueName=topic_name)

            if subscription_name is not None:
                self.subscription_name = subscription_name
                self.subscriber = sqs_resource.get_queue_by_name(
                    QueueName=subscription_name)
        except Exception as e:
            raise Exception("Error in Initializing SQS: {}".format(e))

    def send_message(self, message):
        """Send a message to the queue."""
        if message is None:
            logging.warning('No message to send')
            return
        self.send_messages([message])

    def receive_message(self, Wait_time_seconds=2):
        messages = self.receive_messages(Wait_time_seconds, max_messages=1)
        if messages is not None and len(messages) > 0:
            return messages[0]

    def delete_message(self, message):
        if message is None:
            logging.warning('No message to delete')
            return
        self.delete_messages([message])

    def send_messages(self, messages):
        try:
            if messages is not None and len(messages) > 10:
                raise Exception(
                    "Maximum number of entries per request are 10. You have sent {} messages".format(len(messages)))
            entries = [{
                'Id': str(ind),
                'MessageBody': msg['body']
            } for ind, msg in enumerate(messages)]
            response = self.publisher.send_messages(Entries=entries)
            if 'Failed' in response:
                for msg_meta in response['Failed']:
                    logging.warning(
                        "Failed to send: %s: %s",
                        msg_meta['MessageId'],
                        messages[int(msg_meta['Id'])]['body']
                    )
        except ClientError as error:
            logging.exception(
                "Send messages failed to queue: %s", self.topic_name)
            raise error
        except Exception as e:
            raise Exception("Error in sending messages: {}".format(e))

    def receive_messages(self, Wait_time_seconds=2, max_messages=1):
        if max_messages > 10:
            raise Exception(
                " Value {} for max_messages is invalid. Maximum number of messages that can be received in a single request is 10".format(max_messages))
        messages = []
        response = self.subscriber.receive_messages(
            WaitTimeSeconds=Wait_time_seconds,
            MaxNumberOfMessages=max_messages,
        )
        for message in response:
            messages.append(
                {"body": message.body, "ack_id": message.receipt_handle})
        return messages

    def delete_messages(self, messages):
        try:
            if messages is None:
                logging.warning('No messages to delete')
                return
            entries = [{
                'Id': str(ind),
                'ReceiptHandle': msg["ack_id"]
            } for ind, msg in enumerate(messages) if msg is not None]

            response = self.subscriber.delete_messages(Entries=entries)
            if 'Failed' in response:
                error_message = "Failed to delete messages: {}".format(
                    response)
                raise Exception(error_message)
        except Exception as e:
            raise Exception("Error in deleting messages: {}".format(e))
