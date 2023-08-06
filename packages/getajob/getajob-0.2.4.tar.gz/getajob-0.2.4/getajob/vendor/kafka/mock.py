from kafka import KafkaProducer


class MockKafkaProducer(KafkaProducer):
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        ...

    def send(self, *args, **kwargs):
        ...
