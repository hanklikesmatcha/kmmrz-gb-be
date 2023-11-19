from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from . import Product, User
from typing import TYPE_CHECKING
    
class CheckoutOrder(BaseModel):
    product_name: str
    owner_email: str
    campaign_key: str
    quantity: Decimal
    price: Decimal
    