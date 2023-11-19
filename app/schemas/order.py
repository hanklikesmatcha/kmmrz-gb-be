from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from .product import Product

class OrderStatus(str, Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    CANCELLED = 'CANCELLED'
    REFUNDED = 'REFUNDED'
    
class OrderBase(BaseModel):
    owner_email: Optional[str] = None
    owner_name: Optional[str] = None
    quantity: Decimal


class OrderCreate(OrderBase):
    owner_id: Optional[UUID] = None
    product_id: Optional[str] = None
    campaign_id: Optional[int] = None
    campaign_key: Optional[str] = None  
    
class OrderUpdate(OrderBase):
    id: int
    status: OrderStatus
    
class OrderOwner(BaseModel):
    name: str
    email: str
    
class Order(OrderBase):
    id: int
    total_price: Decimal
    product: Product
    status: OrderStatus
    owner: OrderOwner
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True