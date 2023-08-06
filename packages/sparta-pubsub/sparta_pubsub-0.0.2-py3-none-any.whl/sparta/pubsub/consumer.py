import logging
import sys
from typing import Callable

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message


class PubsubConsumer:
    def __init__(
        self,
        project_id: str,
        subscription_id: str,
        callback: Callable[[Message], None],
        max_messages=1,
    ):
        if not project_id:
            raise ValueError("Missing project_id")
        if not subscription_id:
            raise ValueError("Missing subscription_id")
        if not callback:
            raise ValueError("Missing callback")
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = pubsub_v1.SubscriberClient.subscription_path(
            project_id, subscription_id
        )
        self.flow_control = pubsub_v1.types.FlowControl(max_messages=max_messages)
        self.callback = callback
        self.streaming_pull_future = None
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def shutdown(self):
        if self.streaming_pull_future and self.streaming_pull_future.cancel:
            self._logger.debug(
                f"Stop listening to '{self.subscription_path}'. Shutting down..."
            )
            try:
                self.streaming_pull_future.cancel()  # Trigger the shutdown.
                self.streaming_pull_future.result()  # Block until the shutdown is complete.
                self._logger.debug(f"Shutdown")
            except:
                self._logger.error(f"Shutdown failed due to {sys.exc_info()}")
            finally:
                self.subscriber.close()

    def start(self):
        def _callback_wrapper(message: Message):
            self._logger.debug(
                f"Received"
                f" message_id={message.message_id}"
                f" data={message.data}"
                f" attributes={message.attributes}"
                f" publish_time={message.publish_time}"
                f" ordering_key={message.ordering_key}"
                f" delivery_attempt={message.delivery_attempt}"
            )
            self.callback(message)

        # https://cloud.google.com/pubsub/docs/samples/pubsub-subscriber-flow-settings#pubsub_subscriber_flow_settings-python
        # Limit the subscriber to only have N outstanding messages at a time.
        self.streaming_pull_future = self.subscriber.subscribe(
            self.subscription_path,
            callback=_callback_wrapper,
            flow_control=self.flow_control,
            await_callbacks_on_shutdown=True,
        )
        self._logger.debug(f"Start listening to '{self.subscription_path}'")
        return self.streaming_pull_future
