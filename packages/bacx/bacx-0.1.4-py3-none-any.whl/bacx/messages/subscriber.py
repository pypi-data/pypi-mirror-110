import logging
from typing import Callable, Union

import redis
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message

from bacx.messages.constants import (
    GOOGLE_PROJECT_ID,
    MESSAGE_BROKER,
    MESSAGE_RETRY_COUNT,
    PUBSUB_SUBSCRIPTION_TEMPLATE,
    REDIS_AUTH,
    REDIS_QUEUE_TEMPLATE,
    REDIS_URL,
    MessageBrokers,
)


class BaseSubscriberClient:
    def blocking_subscribe(self, channel: str, callback: Callable):
        raise NotImplementedError


class MissingSubscriberClient(BaseSubscriberClient):
    def blocking_subscribe(self, channel: str, callback: Callable):
        raise ValueError("Missing MESSAGE_BROKER environment variable")


class GooglePubSubSubscriberClient(BaseSubscriberClient):
    def __init__(self):
        self.client = pubsub_v1.SubscriberClient()
        if not GOOGLE_PROJECT_ID:
            raise ValueError("Missing GOOGLE_PROJECT_ID environment variable")
        self.project_id = GOOGLE_PROJECT_ID

    def blocking_subscribe(self, channel: str, callback: Callable):
        subscription_path = self.client.subscription_path(
            self.project_id, PUBSUB_SUBSCRIPTION_TEMPLATE.format(type=channel)
        )
        streaming_pull_future = self.client.subscribe(
            subscription_path, callback=callback, flow_control=pubsub_v1.types.FlowControl(max_messages=1)
        )
        logging.info(f"Worker subscribed")
        with self.client:
            try:
                streaming_pull_future.result()
            except Exception as e:
                streaming_pull_future.cancel()
                print(f"Listening for messages on {subscription_path} threw an exception: {e}.")


class RedisSubscriberClient(BaseSubscriberClient):
    RETRY_COUNT = MESSAGE_RETRY_COUNT

    class MessageWrapper:
        """
        Pretend to be google.cloud.pubsub_v1.subscriber.message.Message
        """

        def __init__(self, data):
            self._data = data
            self.retries = RedisSubscriberClient.RETRY_COUNT
            self.is_acked = False
            self.message_id = "--"

        @property
        def data(self):
            return self._data

        def ack(self):
            """This will remove the message from its queue."""
            self.is_acked = True

        def nack(self):
            """This will keep the message in its queue, but will decrease the retry counter"""
            if self.retries >= 0:
                self.retries -= 1

        def modify_ack_deadline(self, seconds):
            """No deadlines in Redis for now"""
            pass

    def __init__(self):
        self.redis = redis.Redis(REDIS_URL, password=REDIS_AUTH)

    def _consume_queue(self, queue: str, callback: Callable):
        while self.redis.llen(queue) > 0:
            logging.info(f"Processing message from queue {queue}")
            message = RedisSubscriberClient.MessageWrapper(self.redis.lindex(queue, -1))
            while not message.is_acked:
                callback(message)
                if message.retries < 0:
                    break
                if not message.is_acked:
                    logging.info(f"Received nack(), retries remaining {message.retries}")
            self.redis.rpop(queue)

    def blocking_subscribe(self, channel: str, callback: Callable):
        queue_name = REDIS_QUEUE_TEMPLATE.format(type=channel)
        active_queue = f"{queue_name}--active"
        self._consume_queue(active_queue, callback)

        while True:
            logging.info(f"Waiting for new message in queue {queue_name}")
            self.redis.brpoplpush(queue_name, active_queue)
            self._consume_queue(active_queue, callback)


TMessage = Union[Message, RedisSubscriberClient.MessageWrapper]


_the_subscriber_class = {
    MessageBrokers.NONE: MissingSubscriberClient,
    MessageBrokers.REDIS: RedisSubscriberClient,
    MessageBrokers.GOOGLE_PUBSUB: GooglePubSubSubscriberClient,
}[MESSAGE_BROKER]

the_subscriber = _the_subscriber_class()
