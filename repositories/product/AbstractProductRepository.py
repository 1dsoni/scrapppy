import abc

from models import Product


class AbstractProductRepository(abc.ABC):

    @abc.abstractmethod
    def save(self, product: Product) -> Product:
        pass
