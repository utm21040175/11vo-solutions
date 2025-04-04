from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from products.models.cart import Cart
from products.models.products import Product
from products.schemas.cart import CartItem, CartResponse
from products.services.cart import add_to_cart, remove_from_cart, get_cart
from login.core.security import get_current_user
from login.models.user import User

router = APIRouter()

@router.post("/add-to-cart", response_model=CartResponse, status_code=201)
def add_product_to_cart(cart_data: CartItem, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    cart_item = add_to_cart(db, user.id, cart_data.product_id, cart_data.quantity)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found")
    return cart_item

@router.get("/view-cart", response_model=CartResponse)
def view_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart_data = get_cart(db, user.id)
    
    if not cart_data:
        raise HTTPException(status_code=404, detail="Cart is empty")

    return cart_data

@router.delete("/remove-from-cart/{product_id}", status_code=204)
def remove_product_from_cart(product_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    success = remove_from_cart(db, user.id, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"detail": "Product removed from cart successfully"}