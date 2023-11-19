from sqlalchemy import Boolean, Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Base

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=text("gen_random_uuid()"))
    # Google OAuth2
    name = Column(String, default="", nullable=False)
    email = Column(String, unique=True, index=True)
    image = Column(String, nullable=True)
    expires = Column(DateTime, nullable=True)
    session_token = Column(String, nullable=True) 
    
    source = Column(String, default="GOOGLE")
    is_active = Column(Boolean, default=True)

    user_type = Column(String, default="CONSUMER")
    role = Column(String, default="USER")

    orders = relationship("Order", back_populates="owner")
    campaigns = relationship("Campaign", back_populates="owner")
