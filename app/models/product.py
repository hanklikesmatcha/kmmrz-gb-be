from sqlalchemy import DECIMAL, Column, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from models import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String, nullable=True)
    brand_url = Column(String, nullable=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    retail_price = Column(DECIMAL, nullable=True)
    price = Column(DECIMAL, nullable=False)
    discount = Column(DECIMAL, nullable=True)
    image = Column(String, nullable=True)
    
    orders = relationship("Order", back_populates="product")
    campaigns = relationship("Campaign", back_populates="product")
