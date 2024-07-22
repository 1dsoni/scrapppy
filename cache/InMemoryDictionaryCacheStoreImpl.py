import asyncio
from collections import defaultdict
from typing import Dict, Any

from cache.AbstractCacheStore import AbstractCacheStore
from singleton_mixin import SingletonMixin


class InMemoryDictionaryCacheStoreImpl(AbstractCacheStore, SingletonMixin):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._dict: Dict[Any, Any] = defaultdict()
            self._lock = asyncio.Lock()

    async def get(self, key: str) -> bytes:
        async with self._lock:
            return self._dict.get(key)

    async def set(self, key: str, value: str, expiry_ttl_in_seconds: float = None) -> None:
        async with self._lock:
            self._dict[key] = value

    async def delete(self, key: Any) -> None:
        async with self._lock:
            if key in self._dict:
                del self._dict[key]
