import abc
from typing import List

from models import Product


class AbstractProductRepository(abc.ABC):

    @abc.abstractmethod
    async def save(self, product: Product) -> Product:
        pass

    @abc.abstractmethod
    async def fetch_all(self) -> List[Product]:
        pass
