import json
from kafka import KafkaProducer

from getajob.vendor.kafka.kafka import produce_message
from getajob.vendor.kafka.models import KafkaTopic, BaseKafkaMessage


class KafkaRepository:
    def __init__(self, producer: KafkaProducer):
        self.producer = producer

    def publish(self, topic: KafkaTopic, message: BaseKafkaMessage) -> None:
        produce_message(self.producer, topic, json.dumps(message.dict(), default=str))

    def disconnect(self):
        if type(self.producer) == KafkaProducer:
            self.producer.flush()
            self.producer.close()
