from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).one_or_none()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, expires=user.expires)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_order_by_id(db: Session, order_id: int):
    return (
        db.query(models.Order)
        .filter(models.Order.id == order_id)
        .one_or_none()
    )
def create_user_order(db: Session, order: schemas.OrderCreate):
    total_price = order.price * order.quantity
    orderCampaign = (
        db.query(models.Campaign)
        .filter(models.Campaign.key == order.campaign_key)
        .one_or_none()
    )
    orderUser = db.query(models.User).filter(models.User.email == order.owner_email).one_or_none()
    db_order = models.Order(
        owner_id=orderUser.id,
        product_id=orderCampaign.product_id,
        campaign_id=orderCampaign.id,
        quantity=order.quantity,
        total_price=total_price,
        status='PENDING',
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_user_order(db: Session, order: schemas.OrderUpdate):
    db_order = (
        db.query(models.Order)
        .filter(models.Order.id == order.id)
        .one_or_none()
    )
    db_order.status = order.status
    db.commit()
    db.refresh(db_order)
    return db_order


def create_user_campaign(db: Session, campaign: schemas.CampaignCreate):
    db_campaign = models.Campaign(**campaign.model_dump())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


def get_campaigns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Campaign).offset(skip).limit(limit).all()


def get_campaign_by_key(db: Session, campaign_key: str):
    return (
        db.query(models.Campaign)
        .filter(models.Campaign.key == campaign_key)
        .one_or_none()
    )


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_user_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
