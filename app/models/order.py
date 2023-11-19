from sqlalchemy import Column, ForeignKey, Integer, DECIMAL, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from models import Base

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))  # Use UUID data type
    product_id = Column(Integer, ForeignKey("product.id"))
    campaign_id = Column(Integer, ForeignKey("campaign.id"), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    total_price = Column(DECIMAL, default=0, nullable=False)
    # Help me to change status to ENUM type with 'pending', 'paid', 'cancelled', 'refunded'
    status = Column(Enum('PENDING', 'PAID', 'CANCELLED', 'REFUNDED', name='status_enum'), default='PENDING', nullable=False)

    
    owner = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    campaign = relationship("Campaign", back_populates="orders")