from constants import BASE_DIR
from repositories.product.AbstractProductRepository import AbstractProductRepository
from repositories.product.ProductRepositoryLocalFileImpl import ProductRepositoryLocalFileImpl
from repositories.product.ProductRepositoryPGImpl import ProductRepositoryPGImpl
from repositories.product.constants import ProductRepositoryBackend


class ProductRepositoryFactory:

    @staticmethod
    def get_repository(backend: str) -> AbstractProductRepository:
        if backend == ProductRepositoryBackend.postgres:
            return ProductRepositoryPGImpl()
        elif backend == ProductRepositoryBackend.local_file_as_db:
            return ProductRepositoryLocalFileImpl(file_path=BASE_DIR.joinpath("products.json"))

        raise NotImplementedError(f"repository not implemented for backend={backend}")
