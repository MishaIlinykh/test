from db.storages.cache_storage import RedisCache
from db.connections.redis import get_redis
from broker.kafka_init import get_kafka
from services.track_service import TrackService
from services.kafka_producer import KafkaEventProducer


def get_track_service() -> TrackService:
    cache = RedisCache(get_redis())
    return TrackService(cache=cache)


def get_kafka_service() -> KafkaEventProducer:
    kafka_producer = get_kafka()
    return KafkaEventProducer(kafka_producer=kafka_producer)
