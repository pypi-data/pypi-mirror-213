
from cloudservices.config import cloud_config

from pyparsing import abstractmethod


class Queue:
    """
    Initializes the appropriate queue client instance based on the cloud provider.

    Args:
        topic_name (str, optional): The name of the topic to subscribe to. Defaults to None.
        subscription_name (str, optional): The name of the subscription to use. Defaults to None.

    Returns:
        None: The appropriate queue client instance is initialized.

    Examples:
    ---------

    Initialize a `Queue` instance for interacting with an AWS SQS queue named 'my-queue':
    ```
    queue = Queue(subscription_name='my-queue', topic_name='my-topic')
    ```

    Initialize a `Queue` instance for interacting with a GCP PubSub topic named 'my-topic' and subscription named 'my-subscription':
    ```
    queue = Queue(subscription_name='my-subscription', topic_name='my-topic')
    ```
    """

    def __init__(self, topic_name=None, subscription_name=None):

        cloud_provider = cloud_config.cloud_provider
        if cloud_provider == 'AWS':
            # Set up SQS
            from .sqs import SQS
            sqs_client = SQS(
                subscription_name=subscription_name, topic_name=topic_name)
            self.client = sqs_client

        elif cloud_provider == 'GCP':
            # Set up PubSub
            from .pubsub import PubSub
            pubsub_client = PubSub(
                topic_name=topic_name, subscription_name=subscription_name)
            self.client = pubsub_client
        else:
            raise ValueError(f"Unsupported cloud provider: {cloud_provider}")

    @abstractmethod
    def send_message(self, message):
        """Send a message to the queue.

        Args:
            message (dict): The message to delete from the queue.

            format: `{"body": "hello"}`

        """
        raise NotImplementedError(
            "send_message is not implemented for this queue client.")

    @abstractmethod
    def receive_message(self, Wait_time_seconds=2):
        """Receive a message from the queue.

        Args:
            Wait_time_seconds (int, optional): The number of seconds to wait for a message to arrive. Defaults to 2.

        Returns:
            A message from the queue.
            format: `{"body": "hello", "ack_id": "1234"}`

        ```
        """
        raise NotImplementedError(
            "receive_message is not implemented for this queue client.")

    @abstractmethod
    def delete_message(self, message):
        """Delete a message from the queue.

        Args:
            message (dict): The message to delete from the queue.

            format: `{"body": "hello", "ack_id": "1234"}`

        Returns:
            None
        """
        raise NotImplementedError(
            "delete_message is not implemented for this queue client.")

    @abstractmethod
    def send_messages(self, messages):
        """Send multiple messages to the queue.

        Args:
            messages (list): A list of messages to send.

        Args:
            message (dict): The message to delete from the queue.

            format: `[{"body": "hello"}]`

        Returns:
            None
        """
        raise NotImplementedError(
            "send_messages is not implemented for this queue client.")

    @abstractmethod
    def receive_messages(self, Wait_time_seconds=2, max_messages=10):
        """Receive multiple messages from the queue.

        Args:
            Wait_time_seconds (int, optional): The number of seconds to wait for a message to arrive. Defaults to 2.
            max_messages (int, optional): The maximum number of messages to receive. Defaults to 10.

        Returns:
            A list of messages from the queue.

            sample : `[{"body": "hello", "ack_id": "1234"}, {"body": "world", "ack_id": "5678"}]`
        """
        raise NotImplementedError(
            "receive_messages is not implemented for this queue client.")

    @abstractmethod
    def delete_messages(self, messages):
        """Delete multiple messages from the queue.

        Args:
            messages (list): A list of messages to delete.

        Returns:
            None
        """
        raise NotImplementedError(
            "delete_messages is not implemented for this queue client.")
