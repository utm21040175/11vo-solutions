from pydantic import BaseModel
from typing import List, Optional

class CartItem(BaseModel):
    product_id: int
    quantity: int
    
class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItem]
    total_price: float
    
    class Config:
        orm_mode = True