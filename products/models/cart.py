from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from core.database import Base

class Cart(Base):
    __tablename__ = 'cart'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('produccts.id'), nullable=False)
    quantity = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)
    
    user = relationship('User', back_populates='cart')
    product = relationship("Product", back_populates="cart_items")