from decimal import Decimal
import json
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
import stripe
from database import SessionLocal
from crud import create_user_order
from config import settings
from schemas.payment import CheckoutOrder

stripe.api_key = settings.stripe_secret_key

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
    responses={500: {"message": "Internal Server Error"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def calculate_total_amount(items):
    total = 0
    for item in items:
        total += item["price"] * item["quantity"]
    
    return Decimal(total * 100)

@router.post("/create")
async def create_payment(order: CheckoutOrder, db: Session = Depends(get_db)):
    try:
        new_order = create_user_order(db=db, order=order)        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error - {str(e)}")

    
    mappedItems = [{
            'price_data': {
                'currency': 'nzd',
                'product_data': {
                'name': order.product_name,
                },
                'unit_amount': int(order.price * 100),
            },
            'quantity': int(order.quantity),
            }]
    
    try:
        session = stripe.checkout.Session.create(
            line_items=mappedItems,
            mode='payment',
            success_url=f'http://localhost:5173/payments/success?order_id={new_order.id}',
            cancel_url='http://localhost:5173/payments/cancel',
        )

        return json.dumps({"url":session.url})
    except Exception as e:
        return json.dumps({"error": str(e)}), 403
