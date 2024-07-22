from pydantic import BaseModel


class Product(BaseModel):
    uid: str
    project: str
    catalog: str
    title: str
    currency: str
    price: float
    image: str
