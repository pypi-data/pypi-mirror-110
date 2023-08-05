import logging

import redis
from google.cloud import pubsub_v1

from bacx.messages.constants import (
    GOOGLE_PROJECT_ID,
    MESSAGE_BROKER,
    PUBSUB_TOPIC_TEMPLATE,
    REDIS_AUTH,
    REDIS_QUEUE_TEMPLATE,
    REDIS_URL,
    MessageBrokers,
)


class BasePublisherClient:
    def publish(self, channel: str, message: bytes):
        raise NotImplementedError


class MissingPublisherClient(BasePublisherClient):
    def publish(self, channel: str, message: bytes):
        raise ValueError("Missing MESSAGE_BROKER environment variable")


class GooglePubSubPublisherClient(BasePublisherClient):
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        if not GOOGLE_PROJECT_ID:
            raise ValueError("Missing GOOGLE_PROJECT_ID environment variable")
        self.project_id = GOOGLE_PROJECT_ID

    def publish(self, channel: str, message: bytes):
        topic_path = self.publisher.topic_path(self.project_id, PUBSUB_TOPIC_TEMPLATE.format(type=channel))
        publisher_future = self.publisher.publish(topic_path, data=message)
        return publisher_future.result()  # Can result in a HTTP server error if this fails, which is OK.


class RedisPublisherClient(BasePublisherClient):
    def __init__(self):
        self.redis = redis.Redis(REDIS_URL, password=REDIS_AUTH)

    def publish(self, channel: str, message: bytes):
        queue_name = REDIS_QUEUE_TEMPLATE.format(type=channel)
        logging.info(f"Pushing message {message} to queue {queue_name}")
        return self.redis.lpush(queue_name, message)


_the_publisher_class = {
    MessageBrokers.NONE: MissingPublisherClient,
    MessageBrokers.REDIS: RedisPublisherClient,
    MessageBrokers.GOOGLE_PUBSUB: GooglePubSubPublisherClient,
}[MESSAGE_BROKER]

the_publisher = _the_publisher_class()
