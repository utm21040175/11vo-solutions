from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., example="Gamming Laptop")
    description: Optional[str] = Field(None, example="Laptop with RTX 4060 and Ryzen 7")
    price: float = Field(..., example=15000.00)
    stock: int = Field(..., example=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    
class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    
class ProductResponse(ProductBase):
    id: int
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True