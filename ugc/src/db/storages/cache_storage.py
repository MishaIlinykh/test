import json
import backoff
from redis import Redis
from typing import Any
from abc import ABC, abstractmethod


class CacheStorage(ABC):
    @abstractmethod
    def get(self, key: str) -> Any | None:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, expire: int):
        pass


class RedisCache(CacheStorage):
    def __init__(self, redis: Redis):
        if redis is None:
            raise ValueError("Redis instance is None!")
        self.redis = redis

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def get(self, key: str) -> Any | None:
        result = self.redis.get(key)
        return json.loads(result) if result else None

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def set(self, key: str, value: Any, expire: int) -> None:
        self.redis.set(key, json.dumps(value), ex=expire)

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def incr(self, key: str) -> int:
        return self.redis.incr(key)

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def expire(self, key: str, seconds: int) -> None:
        self.redis.expire(key, seconds)
