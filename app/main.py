from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Query, Response, Request, Body
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers import payment


app = FastAPI()
app.include_router(payment.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)

    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/user/email", response_model=schemas.User)
def read_user_by_email(email: str = Query(..., example='text@example.com'), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/orders", response_model=schemas.Order)
def create_order_for_user(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_user_order(db=db, order=order)

@app.post("/orders/", response_model=schemas.Order)
def update_order(order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    return crud.update_user_order(db=db, order=order)

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.get("/orders/{order_id}", response_model=schemas.Order)
def find_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id=order_id)
    return order

@app.post("/users/campaigns/", response_model=schemas.Campaign)
def create_campaign_for_user(campaign: schemas.CampaignCreate, db: Session = Depends(get_db)):
    return crud.create_user_campaign(db=db, campaign=campaign)

@app.get("/campaigns/", response_model=list[schemas.Campaign])
def read_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    campaigns = crud.get_campaigns(db, skip=skip, limit=limit)
    return campaigns

@app.get("/campaigns/{campaign_key}", response_model=Optional[schemas.Campaign])
def read_campaign_by_key(campaign_key: str, db: Session = Depends(get_db)):
    campaign = crud.get_campaign_by_key(db, campaign_key=campaign_key)
    return campaign

@app.post("/products/", response_model=schemas.Product)
def create_product_for_user(product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    return crud.create_user_product(db=db, product=product)

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000, log_level="info")