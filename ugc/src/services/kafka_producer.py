from kafka import KafkaProducer
from kafka.errors import KafkaError
from core.config import GeneralConfig


settings = GeneralConfig()


class KafkaEventProducer:
    def __init__(
        self, kafka_producer: KafkaProducer, topic: str = settings.TOPIC_KAFKA
    ):
        self.producer = kafka_producer
        self.topic = topic

    def send(self, event: dict):
        try:
            self.producer.send(self.topic, value=event).get(timeout=5)
        except KafkaError as e:
            raise RuntimeError(f"Ошибка при отправке события в Kafka: {e}")

    def close(self):
        self.producer.close()
