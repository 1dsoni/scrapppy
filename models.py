from pydantic import BaseModel


class ProductScraperConfig(BaseModel):
    max_page: int
    proxy: str


class Product(BaseModel):
    uid: str
    project: str
    catalog: str
    title: str
    currency: str
    price: float
    image: str
