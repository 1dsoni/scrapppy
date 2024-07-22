import abc


class AbstractCacheStore(abc.ABC):

    @abc.abstractmethod
    async def set(self, key: str, value: str, expiry_ttl_in_seconds: float = None) -> None:
        pass

    @abc.abstractmethod
    async def get(self, key: str) -> bytes:
        pass

    @abc.abstractmethod
    async def delete(self, key: str) -> None:
        pass
