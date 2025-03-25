from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum

# Define aviable roles as schema for validation
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

# User schema for creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool
    role: UserRole
    
    @field_validator("role", mode="before")
    @classmethod
    def validate_roles(cls, v):
        if isinstance(v, str):
            v = v.lower()
        return UserRole(v)

# Schema to return user without password
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    role: UserRole
    
    class Config:
        from_atributtes = True # Allows to convert SALAlchemy objects to Pydantic

class UserLogin(BaseModel):
    email: str
    password: str
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str    