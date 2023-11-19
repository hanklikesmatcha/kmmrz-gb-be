from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from . import Product


class CampaignBase(BaseModel):
    name: str
    description: str
    is_active: bool
    start_date: datetime
    end_date: datetime
    product_id: int
    owner_id: UUID
    key: str
    return_time: Optional[int]
    pick_up_time: Optional[datetime]

class CampaignCreate(CampaignBase):
    pass

class CampaignOrder(BaseModel):
    id: int
    total_price: Decimal
    quantity: Decimal
    owner_id: UUID
    

class Campaign(CampaignBase):
    id: int
    product: Product
    orders: list[CampaignOrder]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True