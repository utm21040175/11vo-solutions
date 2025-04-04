from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class OrderCreate(BaseModel):
    total_amount: float
    payment_method: Literal["stripe"] = "stripe"
    payment_status: Literal["pending", "completed", "failed"] = "pending"

    class Config:
        orm_mode = True
        
class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    payment_method: str
    payment_status: str
    created_at: datetime

    class Config:
        orm_mode = True