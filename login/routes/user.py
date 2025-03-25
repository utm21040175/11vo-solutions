from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from login.schemas.user import UserCreate, UserResponse
from login.services.user import create_user

router = APIRouter()

@router.post("/register-user", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user_data)
    
    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    return new_user