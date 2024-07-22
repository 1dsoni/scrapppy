from cache.AbstractCacheStore import AbstractCacheStore
from cache.InMemoryDictionaryCacheStoreImpl import InMemoryDictionaryCacheStoreImpl
from cache.RedisCacheStoreImpl import RedisCacheStoreImpl
from cache.constants import CacheStoreBackend


class CacheStoreFactory:

    @staticmethod
    def get_store(backend) -> AbstractCacheStore:
        if backend == CacheStoreBackend.redis:
            return RedisCacheStoreImpl()
        elif backend == CacheStoreBackend.in_memory_dict:
            return InMemoryDictionaryCacheStoreImpl()

        raise NotImplementedError(f"store not implemented for backend={backend}")
