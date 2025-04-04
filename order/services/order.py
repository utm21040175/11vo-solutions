from sqlalchemy.orm import Session
from datetime import datetime

from core.database import get_db
from order.models.order import Order
from products.models.cart import Cart
from products.models.products import Product
from dotenv import load_dotenv
import stripe
import os

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_order(db: Session, user_id: int):

    cart_items = (
        db.query(Cart)
        .filter(Cart.user_id == user_id)
        .join(Product)
        .all()
    )

    if not cart_items:
        return None

    total = sum(item.product.price * item.quantity for item in cart_items)

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
            currency="usd",
            payment_method_types=["card"],
            description=f"Compra de usuario ID {user_id}",
        )
    except Exception as e:
        print(f"Error en el pago: {str(e)}")
        return {"error": "Error al procesar el pago"}


    new_order = Order(
        user_id=user_id,
        total_amount=total,
        payment_method="stripe",
        payment_status="completed",
        created_at=datetime.utcnow()
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Vaciar el carrito
    for item in cart_items:
        db.delete(item)
    db.commit()

    return new_order
