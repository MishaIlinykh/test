from db.connections.redis import get_redis
from db.storages.cache_storage import RedisCache


def get_cache_storage() -> RedisCache:
    redis = get_redis()
    return RedisCache(redis)
