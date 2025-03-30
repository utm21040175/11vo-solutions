from sqlalchemy import Column, Integer, String, Boolean, Enum, Index
from sqlalchemy.orm import relationship
from core.database import Base
import enum

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, nullable=False)
    Index("is_user_email", email)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.USER)