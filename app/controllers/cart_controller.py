from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.schema import Cart

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add_to_cart/{user_id}/{product_id}")
def add_to_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    # Prevent duplicate entries
    exists = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
    if not exists:
        cart_item = Cart(user_id=user_id, product_id=product_id)
        db.add(cart_item)
        db.commit()
    return RedirectResponse(url=f"/profile/{user_id}", status_code=303)

@router.post("/remove_from_cart/{user_id}/{product_id}")
def remove_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
    if cart_item:
        db.delete(cart_item)
        db.commit()
    return RedirectResponse(url=f"/profile/{user_id}", status_code=303)
