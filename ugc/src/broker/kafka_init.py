from kafka import KafkaProducer
from core.config import GeneralConfig
import json
from datetime import datetime


_kafka: KafkaProducer | None = None
config = GeneralConfig()


def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def get_kafka() -> KafkaProducer:
    global _kafka
    if _kafka is None:
        _kafka = KafkaProducer(
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v, default=json_serializer).encode(
                "utf-8"
            ),
        )
    return _kafka
