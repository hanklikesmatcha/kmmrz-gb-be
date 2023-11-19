from sqlalchemy.orm import registry

mapper_registry = registry()
Base = mapper_registry.generate_base()

from models.user import User
from models.order import Order
from models.product import Product
from models.campaign import Campaign
