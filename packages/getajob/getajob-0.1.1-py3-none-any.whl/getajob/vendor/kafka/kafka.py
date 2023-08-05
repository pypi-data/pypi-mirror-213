from kafka import KafkaProducer, KafkaConsumer

from getajob.config.settings import SETTINGS
from .models import KafkaTopic
from .authentication import generate_kafka_jwt
from .mock import MockKafkaProducer


def get_producer():
    if not SETTINGS.ENABLED_KAFKA_EVENTS:
        return MockKafkaProducer()
    return KafkaProducer(
        bootstrap_servers=[SETTINGS.KAFKA_BOOTSTRAP_SERVER],
        sasl_mechanism="SCRAM-SHA-256",
        security_protocol="SASL_SSL",
        sasl_plain_username=SETTINGS.KAFKA_USERNAME,
        sasl_plain_password=SETTINGS.KAFKA_PASSWORD,
    )


def get_consumer():
    consumer = KafkaConsumer(
        bootstrap_servers=[SETTINGS.KAFKA_BOOTSTRAP_SERVER],
        sasl_mechanism="SCRAM-SHA-256",
        security_protocol="SASL_SSL",
        sasl_plain_username=SETTINGS.KAFKA_USERNAME,
        sasl_plain_password=SETTINGS.KAFKA_PASSWORD,
        auto_offset_reset="earliest",
        group_id="default",
    )
    consumer.subscribe(KafkaTopic.get_all_topics())
    return consumer


def produce_message(producer: KafkaProducer, topic: KafkaTopic, message_json: str):
    message_token = generate_kafka_jwt()
    producer.send(
        topic.value,
        message_json.encode("utf-8"),
        headers=[("authorization", message_token.encode("utf-8"))],
    )
