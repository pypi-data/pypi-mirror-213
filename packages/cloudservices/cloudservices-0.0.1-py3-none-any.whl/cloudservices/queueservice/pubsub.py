import logging
from google.cloud import pubsub_v1
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from google.api_core.exceptions import DeadlineExceeded
import re
from concurrent import futures
from google.cloud import pubsub_v1
from .queue import Queue
from cloudservices.config import cloud_config
from google.auth import default

SUBSCRIPTION_REGEXP = 'projects/([^/]+)/subscriptions/(.+)'
TOPIC_REGEXP = 'projects/([^/]+)/topics/(.+)'


class PubSub(Queue):
    def __init__(self, topic_name=None, subscription_name=None):

        if topic_name is None and subscription_name is None:
            raise ValueError(
                'Either topic_name or subscription_name must be provided.')
        try:
            credentials = None
            if cloud_config.gcp_token_source =="custom":
                credentials = service_account.Credentials.from_service_account_info(
                    cloud_config.gcp_service_account_key_json)
            else:
                # Authenticate using default credentials Workload Identity 
                credentials, _ = default()
            
            if topic_name is not None:
                self.topic_name = self._validate_topic_name(topic_name)
                self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
            if subscription_name is not None:
                self.subscription_name = self._validate_subscription_name(subscription_name)
                self.subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
        except Exception as e:
            raise Exception("Error in Initializing PubSub: {}".format(e))

    def send_message(self, message):
        try:
            data = message.get("body").encode("utf-8")
            publish_future = self.publisher.publish(self.topic_name, data)
            future = publish_future.result()
            if future is None:
                logging.warn("Could not send message: {}".format(message))

        except Exception as e:
            raise Exception("Error sending message: {}".format(e))

    def receive_message(self, Wait_time_seconds=2):
        messages = self.receive_messages(Wait_time_seconds, max_messages=1)
        if messages is not None and len(messages) > 0:
            return messages[0]

    def delete_message(self, message):
        self.delete_messages([message])

    def send_messages(self, messages):
        try:
            if messages is None or len(messages) > 1000:
                raise Exception(
                    "Maximum number of entries per request are 1000. You have sent {} messages".format(len(messages)))
            publish_futures = []

            def callback(future: pubsub_v1.publisher.futures.Future) -> None:
                future = future.result()
                if future is None:
                    logging.warn("Could not send message: {}".format(message))

            for message in messages:
                data = message.get("body").encode("utf-8")
                publish_future = self.publisher.publish(self.topic_name, data)
                publish_future.add_done_callback(callback)
                publish_futures.append(publish_future)

            futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        except Exception as e:
            raise Exception("Error sending messages: {}".format(e))

    def receive_messages(self, Wait_time_seconds=2, max_messages=1):
        try:
            messages = []
            response = self.subscriber.pull(
                subscription=self.subscription_name,
                max_messages=max_messages,
                timeout=Wait_time_seconds,
            )

            received_messages = response.received_messages
            for message in received_messages:
                messages.append({"body": message.message.data.decode(
                    "utf-8"), "ack_id": message.ack_id})
            return messages
        except DeadlineExceeded:
            pass
        except Exception as e:
            raise Exception("Error receiving messages: {}".format(e))

    def delete_messages(self, messages):
        try:
            if messages is None:
                raise ValueError("messages cannot be None")

            ack_ids = []
            for message in messages:
                ack_ids.append(message["ack_id"])
            if len(ack_ids) == 0:
                return

            self.subscriber.acknowledge(
                subscription=self.subscription_name, ack_ids=ack_ids)
        except Exception as e:
            raise Exception("Error deleting messages: {}".format(e))

    def _validate_topic_name(self, topic_name):
        match = re.match(TOPIC_REGEXP, topic_name)
        if not match:
            raise ValueError(
                'Invalid topic name: %r, should be of the format projects/{project_id}/topics/{topic_name}' % topic_name)
        return topic_name

    def _validate_subscription_name(self, subscription_name):
        match = re.match(SUBSCRIPTION_REGEXP, subscription_name)
        if not match:
            raise ValueError(
                'Invalid subscription name: %r, should be of the format projects/{project_id}/subscriptions/{subscription_name}' % subscription_name)
        return subscription_name
