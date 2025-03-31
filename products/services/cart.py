from sqlalchemy.orm import Session
from products.models.cart import Cart
from products.models.products import Product

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    # Check if the product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None  # Product not found

    # Check if the user already has a cart entry for this product
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()

    if cart_item:
        # Update the quantity and total price if the item already exists in the cart
        cart_item.quantity += quantity
        cart_item.total_price = cart_item.quantity * product.price
    else:
        # Create a new cart item
        cart_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=quantity * product.price
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item

def remove_from_cart(db: Session, user_id: int, product_id: int):
    # Find the cart item
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()

    if not cart_item:
        return None  # Cart item not found

    db.delete(cart_item)
    db.commit()
    return True  # Successfully removed from cart