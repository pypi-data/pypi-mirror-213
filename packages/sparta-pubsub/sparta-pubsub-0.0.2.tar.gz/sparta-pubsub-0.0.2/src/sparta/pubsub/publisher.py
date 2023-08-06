import logging

from google.cloud import pubsub_v1


class PubsubPublisher:
    def __init__(self, project_id: str, topic_id: str, enable_message_ordering=None):
        publisher_options = pubsub_v1.types.PublisherOptions(
            enable_message_ordering=enable_message_ordering
        )
        self.publisher = pubsub_v1.PublisherClient(publisher_options=publisher_options)
        self.topic_path = self.publisher.topic_path(project_id, topic_id)
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def publish_and_wait_for_message_id(self, data: bytes, ordering_key=None, **attrs):
        future = self._publish(data, ordering_key, **attrs)
        message_id = future.result()
        self._logger.debug(f"Published data={data} > message_id={message_id} ")
        return message_id

    def publish(self, data: bytes, ordering_key=None, **attrs):
        future = self._publish(data, ordering_key, **attrs)
        self._logger.debug(f"Published data={data}")
        return future

    def _publish(self, data: bytes, ordering_key=None, **attrs):
        _attrs = {
            k: v for k, v in attrs.items() if v is not None and isinstance(v, str)
        }
        return self.publisher.publish(
            topic=self.topic_path,
            data=data,
            ordering_key=ordering_key if ordering_key else "",
            **_attrs,
        )
