from kafka import KafkaProducer


class MockKafkaProducer(KafkaProducer):
    def __init__(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs):
        pass
