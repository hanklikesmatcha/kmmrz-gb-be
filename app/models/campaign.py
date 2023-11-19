from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models import Base


class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # For url slug
    key = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    pick_up_time = Column(DateTime, nullable=True)
    # A day period eg, 7 = 7 days.
    return_time = Column(Integer, nullable=True) 
    
    product_id = Column(Integer, ForeignKey("product.id"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))  # Use UUID data type

    product = relationship("Product", back_populates="campaigns")
    owner = relationship("User", back_populates="campaigns")

    orders = relationship("Order", back_populates="campaign")
