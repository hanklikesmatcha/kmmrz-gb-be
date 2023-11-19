from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from .order import Order

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    image: Optional[str] = None
    expires: Optional[datetime]
    user_type: Optional[str] = None
    
class User(UserBase):
    id: UUID
    is_active: bool
    user_type: str
    role: str
    items: list[Order] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True