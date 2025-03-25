from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from login.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from login.models.user import User
from login.services.user import create_user
from login.core.passwords import verify_password
from login.core.security import create_jwt_token

router = APIRouter()

@router.post("/register-user", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user_data)
    
    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    return new_user

@router.post("/login", response_model=TokenResponse, status_code=200)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_jwt_token(data={"sub": user.email})
    
    return TokenResponse(access_token=access_token, token_type="bearer")