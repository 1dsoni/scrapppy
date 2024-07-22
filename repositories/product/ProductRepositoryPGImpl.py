import logging
from contextlib import asynccontextmanager

import asyncpg

from singleton_mixin import SingletonMixin
from models import Product
from repositories.product.AbstractProductRepository import AbstractProductRepository

logger = logging.getLogger(__name__)


class ProductRepositoryPGImpl(AbstractProductRepository, SingletonMixin):
    _pool = None

    def __init__(self):
        self.database_url = "postgresql://scrapy_rw:password@localhost/scrapy_db"

    async def _init_connection_pool(self):
        if not self._pool:
            self._pool = await asyncpg.create_pool(self.database_url, min_size=1, max_size=10)
            logger.info("initialized pg connection pool")

    async def setup_db(self):
        async with self.get_db_conn() as conn:
            await conn.execute('''
                            CREATE TABLE IF NOT EXISTS products (
                                id SERIAL PRIMARY KEY,
                                uid VARCHAR(64) UNIQUE NOT NULL,
                                project TEXT NOT NULL,
                                catalog TEXT NOT NULL,
                                title TEXT NOT NULL,
                                currency TEXT NOT NULL,
                                price REAL NOT NULL,
                                image TEXT NULL,
                                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                            )
                        ''')

    @asynccontextmanager
    async def get_db_conn(self):
        await self._init_connection_pool()

        async with self._pool.acquire() as conn:
            yield conn

        logger.info("released connection back to connection pool")

    async def save(self, product: Product) -> Product:
        async with self.get_db_conn() as conn:
            await conn.execute('''
                    INSERT INTO products (uid, 
                                          project, 
                                          catalog,
                                          title,
                                          currency,
                                          price,
                                          image)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)''',
                               product.uid,
                               product.project,
                               product.catalog,
                               product.title,
                               product.currency,
                               product.price,
                               product.image)

        return product
