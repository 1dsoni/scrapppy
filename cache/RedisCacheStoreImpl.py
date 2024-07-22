import logging

import redis

from cache.AbstractCacheStore import AbstractCacheStore
from singleton_mixin import SingletonMixin

logger = logging.getLogger(__name__)


class RedisCacheStoreImpl(AbstractCacheStore, SingletonMixin):

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.pool = redis.asyncio.ConnectionPool(host='localhost',
                                                     port=6379,
                                                     db=0,
                                                     max_connections=256)
            self._initialized = True

    def get_client(self) -> redis.asyncio.Redis:
        return redis.asyncio.Redis(connection_pool=self.pool)

    async def set(self, key: str, value: str, expiry_ttl_in_seconds: float = None) -> None:
        await self.get_client().set(name=key, value=value, ex=expiry_ttl_in_seconds)

    async def get(self, key: str) -> bytes:
        return await self.get_client().get(key)

    async def delete(self, key: str) -> None:
        await self.get_client().delete(key)
