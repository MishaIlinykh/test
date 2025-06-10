from typing import Optional
from redis import Redis
from core.config import GeneralConfig

redis: Optional[Redis] = None
config = GeneralConfig()


def get_redis() -> Redis:
    return Redis(config.REDIS_HOST, config.REDIS_PORT)
