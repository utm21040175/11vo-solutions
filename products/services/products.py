from sqlalchemy.orm import Session
from products.models.products import Product
from products.schemas.products import ProductCreate, ProductResponse

def create_product_service(db: Session, product_data: ProductCreate) -> ProductResponse:
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_product_service(db: Session, product_id: int) -> ProductResponse | None:
    return db.query(Product).filter(Product.id == product_id). first()

def get_all_products_service(db: Session, skip: int = 0, limit: int = 10) -> list[ProductResponse]:
    return db.query(Product).offset(skip).limit(limit).all()

def update_product_service(db: Session, product_id: int, product_data: ProductCreate) -> ProductResponse | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    for key, value in product_data.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product_service(db: Session, product_id: int) -> bool:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True