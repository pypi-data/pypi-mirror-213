import os
from google.cloud import pubsub_v1
import google.api_core.exceptions
import json
import traceback
from typing import List

from whitson_tool_helper.messaging.helper import check_environment_variables
from whitson_tool_helper.logger import LOGGER


class PubsubConsumer:
    def __init__(self, process_func, to_dict=False):
        check_environment_variables(
            [
                "GOOGLE_PROJECT",
                "GOOGLE_APPLICATION_CREDENTIALS",
            ]
        )
        self.decode_json = to_dict
        self.process_func = process_func
        self.subscription = os.environ["MESSAGING_SUBSCRIPTION"]

        self.google_project_name = os.environ["GOOGLE_PROJECT"]
        self.subscriber = pubsub_v1.SubscriberClient()

    @property
    def subscription_path(self):
        if self.subscriber:
            return self.subscriber.subscription_path(
                self.google_project_name, self.subscription
            )
        else:
            raise Exception("Pubsub subscriber not yet instantiated")

    def work(self):
        while True:
            LOGGER.info(f"Pulling subscription {self.subscription_path}")
            try:
                response = self.subscriber.pull(
                    subscription=self.subscription_path, max_messages=1
                )
            except google.api_core.exceptions.DeadlineExceeded as e:
                LOGGER.debug(e)
                continue
            except Exception as e:
                LOGGER.error(e)
                raise
            for received_message in response.received_messages:
                msg = received_message.message
                LOGGER.info(
                    f"Received PubSub message {msg.message_id}",
                    {"pubsub_msg_id": msg.message_id},
                )
                data = json.loads(msg.data.decode("utf8"))
                meta_data = msg.attributes
                try:
                    self.process_func(data, meta_data=meta_data)
                except Exception as e:
                    LOGGER.error(e)
                    LOGGER.error(traceback.format_exc())
                    LOGGER.warning(f"ACKING UNPROCESSED MESSAGE: {msg.message_id}")
                else:
                    LOGGER.info(f"ACKING MESSAGE: {msg.message_id}")
                self.subscriber.acknowledge(
                    subscription=self.subscription_path,
                    ack_ids=[received_message.ack_id],
                )


class PubsubPublisher:
    def __init__(self):
        check_environment_variables(["GOOGLE_PROJECT"])
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = os.environ["GOOGLE_PROJECT"]
        self.futures = set()

    @property
    def topic_name(self):
        return f"projects/{self.project_id}/topics/{self.topic}"

    def callback(future: pubsub_v1.publisher.futures.Future) -> None:
        future.result()

    def publish(
        self,
        topic: str,
        payload: dict,
        meta_data: dict = {},
        encode_json=True,
        **kwargs,
    ):
        LOGGER.debug("Publishing single to pubsub")
        self.topic = topic
        payload = json.dumps(payload).encode("utf8") if encode_json else payload
        future = self.publisher.publish(self.topic_name, payload, **meta_data)
        future.result()

    def publish_many(self, topic, payloads: List[dict], **kwargs):
        LOGGER.debug("Publishing many to pubsub")
        self.topic = topic

        for payload in payloads:
            data = json.dumps(payload.get("data")).encode("utf-8")
            meta_data = payload.get("meta_data") or {}
            future = self.publisher.publish(self.topic_name, data, **meta_data)
            future.result()
