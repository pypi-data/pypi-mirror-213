import hashlib
import time
from typing import Optional

import ujson as json
from kafka import KafkaProducer
from kafka.errors import KafkaError
from loguru import logger
from pydantic import BaseModel

from gdshoplib.core.settings import NotionSettings


class Message(BaseModel):
    data: dict
    timestamp: float
    data_md5: Optional[str]
    message_type: str

    def send(self, producer, topic):
        data = json.dumps(self.data, sort_keys=True).encode("utf-8")
        self.data_md5 = hashlib.md5(data).hexdigest()
        future = producer.send(topic, self.dict())
        try:
            future.get(timeout=10)
        except KafkaError as e:
            logger.exception(e)


class Ecosystem:
    _producer = None

    @property
    def producer(self):
        if not self._producer:
            self._producer = KafkaProducer(
                bootstrap_servers=NotionSettings().KAFKA_BROKER,
                value_serializer=lambda m: json.dumps(m, sort_keys=True).encode(
                    "utf-8"
                ),
                request_timeout_ms=1000,
            )
        return self._producer

    def send_message(self, topic, /, data, message_type):
        Message(
            data=data, timestamp=float(time.time()), message_type=message_type
        ).send(self.producer, topic)
        logger.info(f"{time.time()}: {topic}/{message_type}")
