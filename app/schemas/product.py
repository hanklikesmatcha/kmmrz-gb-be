from decimal import Decimal
from typing import Optional, Union
from fastapi import UploadFile

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    brand_name: str
    brand_url: str
    retail_price: Decimal
    description: Union[str, None] = None
    price: Decimal
    discount: Decimal
    image: Optional[str] = None
    file: Optional[UploadFile] = None

class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True