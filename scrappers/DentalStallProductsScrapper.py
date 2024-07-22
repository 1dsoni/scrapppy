import asyncio
import logging
import uuid

import aiohttp
from bs4 import BeautifulSoup

from cache.AbstractCacheStore import AbstractCacheStore
from cache.CacheStoreFactory import CacheStoreFactory
from cache.constants import CacheStoreBackend
from models import Product
from notifications import ConsoleNotifier
from repositories.product.AbstractProductRepository import AbstractProductRepository
from repositories.product.ProductRepositoryFactory import ProductRepositoryFactory
from repositories.product.constants import ProductRepositoryBackend

logger = logging.getLogger(__name__)


class DentalStallProductsScrapper:
    USER_AGENT_HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    PROJECT_NAME = "dental_stall"

    def __init__(self,
                 product_repository: AbstractProductRepository = None,
                 cache: AbstractCacheStore = None,
                 proxy: str = None,
                 max_page: int = 10,
                 page_load_retry_wait: int = 5,
                 max_page_load_retries: int = 1):
        if product_repository:
            self.product_repository = product_repository
        else:
            self.product_repository = ProductRepositoryFactory.get_repository(backend=ProductRepositoryBackend.local_file_as_db)

        if cache:
            self.cache = cache
        else:
            self.cache = CacheStoreFactory.get_store(backend=CacheStoreBackend.in_memory_dict)

        self.proxy = proxy
        self.page_load_retry_wait = page_load_retry_wait
        self.max_page_load_retries = max_page_load_retries
        self.max_page = max_page

    async def scrape(self):
        logger.error("start to scrape")
        session = aiohttp.ClientSession(headers=self.USER_AGENT_HEADER)

        if self.proxy:
            session.proxies = {"http": self.proxy, "https": self.proxy}

        await self._scrape(session)
        await session.close()

    async def _scrape(self, client):
        current_page = 1
        page_load_retry_count = 0

        while True:
            if current_page > self.max_page:
                break

            try:
                async with client.get(f"https://dentalstall.com/shop/page/{current_page}/") as response:
                    if response.status != 200:
                        logger.error(f"request failed got response {await response.text()}, status: {response.status}")
                        raise Exception(f"Failed to fetch the page: {current_page}, err: {response.status}")
                    page_text = await response.text()
            except Exception as e:
                logger.error(f"Error fetching page {current_page}: {e}")
                if page_load_retry_count > self.max_page_load_retries:
                    raise e

                await asyncio.sleep(self.page_load_retry_wait)
                page_load_retry_count += 1
                continue

            is_page_text_processed = await self.process_page_text(page_text)
            if not is_page_text_processed:
                break

            current_page += 1

        ConsoleNotifier().notify(f"scrapping of {self.PROJECT_NAME} is completed")

    async def process_page_text(self, page_text: str) -> bool:
        soup = BeautifulSoup(page_text, "html.parser")
        product_elements = soup.select(".purchasable")

        if not product_elements:
            return False

        for element in product_elements:
            await self.process_product(element)

        return True

    async def process_product(self, element):
        try:
            return await self._process_product(element)
        except Exception as e:
            logger.error("failed to process element %s, err: %s", element, e)

    async def _process_product(self, element):
        img_tag = element.find("img")
        product_title = img_tag.get("title")
        image_url = img_tag.get("data-lazy-src")

        price_box = element.select_one(".mf-product-price-box .price")

        if price_box.select_one("ins .woocommerce-Price-amount"):
            # Extract discounted prices
            current_price_element = price_box.select_one("ins .woocommerce-Price-amount")
        elif price_box.select_one(".woocommerce-Price-amount"):
            # Extract regular price
            current_price_element = price_box.select_one(".woocommerce-Price-amount")
        else:
            logger.error("failed to find the price element")
            return

        currency_symbol = current_price_element.find("span", class_="woocommerce-Price-currencySymbol").text
        current_price = current_price_element.text.replace(currency_symbol, "").strip()

        project = self.PROJECT_NAME
        catalog = "default"

        item_identifier_long = f"{project}-{catalog}-{product_title}"

        uid = str(uuid.uuid5(namespace=uuid.NAMESPACE_OID, name=item_identifier_long))

        product = Product(
            uid=uid,
            project=project,
            catalog=catalog,
            title=product_title,
            currency=currency_symbol,
            price=current_price,
            image=image_url
        )

        if not await self.should_process_product(item_identifier_long, current_price):
            return

        await self.save_product_in_db(product)
        await self.save_product_in_cache(item_identifier_long, product)

    async def should_process_product(self, product_title: str, product_price: float) -> bool:
        cached_value = await self.cache.get(product_title)

        if cached_value:
            can_ignore = str(product_price) in str(cached_value)
            if can_ignore:
                return False

        return True

    async def save_product_in_db(self, product: Product):
        try:
            await self.product_repository.save(product)
        except Exception as e:
            logger.error("failed to save in db %s err %s", product.title, e)

    async def save_product_in_cache(self, item_identifier_long, product: Product):
        try:
            await self.cache.set(item_identifier_long, str(product.price))
        except Exception as e:
            logger.error(f"Error saving product in cache {item_identifier_long}: {e}")

    async def get_scrapped_data(self):
        return await self.product_repository.fetch_all()
