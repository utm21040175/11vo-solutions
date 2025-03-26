from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from products.services.products import *
from products.schemas.products import ProductCreate, ProductResponse
from core.dependencies import get_db

router = APIRouter()

@router.post("/create_product", response_model=ProductResponse, status_code=201)
def create_products(product_data: ProductCreate, db: Session = Depends(get_db)):
    new_product = create_product_service(db, product_data)
    return new_product

@router.get("/products-list", response_model=list[ProductResponse])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = get_all_products_service(db, skip, limit)
    return products

@router.get("/{product_id}", response_model=ProductResponse, status_code=200)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = get_product_service(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/update_product/{product_id}", response_model=ProductResponse, status_code=200)
def update_product(product_id: int, product_data: ProductCreate, db: Session = Depends(get_db)):
    updated_product = update_product_service(db, product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/delete_product/{product_id}", status_code=200)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = delete_product_service(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}