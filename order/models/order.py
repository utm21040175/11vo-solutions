from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String, default="stripe")
    payment_status = Column(String, default="pending")
    created_at = Column(DateTime)
    user = relationship("User", back_populates="orders")
