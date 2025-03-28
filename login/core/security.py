from authlib.jose import jwt
from jose import JWTError
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.dependencies import get_db
from sqlalchemy.orm import Session
from core.database import SessionLocal
from login.models.user import User
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

JWT_CONFIG = {
    "alg": "HS256"
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_jwt_token(data: dict):
    """Create access token to authenticate users

    Args:
        data (dict): data to include in the token
        expires_delta (Optional[str], optional): expiration time. Defaults to None.

    Returns:
        str: access token
    """
    return jwt.encode(JWT_CONFIG, data, SECRET_KEY).decode()

def verify_jwt_token(token: str):
    """Verify if the token is valid

    Args:
        token (str): token to verify

    Returns:
        dict: data included in the token
    """
    try:
        return jwt.decode(token, SECRET_KEY)
    except jwt.InvalidTokenError:
        return None
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current user from token

    Args:
        token (str): token to verify. Defaults to Depends(oauth2_scheme).
        db (Session): database session. Defaults to Depends(get_db).
    Returns:
        User: current user
        HTTPException: if token is invalid
        None: if user not found
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        pyload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_CONFIG])
        user_id: int = pyload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user