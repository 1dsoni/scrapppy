import asyncio
import json
import logging
import os
from typing import Any, Dict, List

import aiofiles

from models import Product
from repositories.product.AbstractProductRepository import AbstractProductRepository
from singleton_mixin import SingletonMixin

logger = logging.getLogger(__name__)


class ProductRepositoryLocalFileImpl(AbstractProductRepository, SingletonMixin):
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._lock = asyncio.Lock()

    async def _initialize_file(self):
        if not os.path.exists(self._file_path):
            async with aiofiles.open(self._file_path, mode='w') as f:
                await f.write('{}')

    async def _read_file(self) -> Dict[str, Any]:
        await self._initialize_file()
        async with aiofiles.open(self._file_path, mode='r') as f:
            content = await f.read()
            return json.loads(content) if content else {}

    async def _write_file(self, data: Dict[str, Any]) -> None:
        await self._initialize_file()
        async with aiofiles.open(self._file_path, mode='w') as f:
            await f.write(json.dumps(data, indent=4))

    async def set(self, key: str, value: Any) -> None:
        async with self._lock:
            data = await self._read_file()
            data[key] = value
            await self._write_file(data)

    async def save(self, product: Product) -> Product:
        await self.set(product.uid, product.dict())
        return product

    async def fetch_all(self) -> List[Product]:
        records = await self._read_file()
        return [Product(**record) for key, record in records.items()]
