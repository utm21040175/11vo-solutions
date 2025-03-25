from sqlalchemy.orm import Session
from models.user import User, UserRole
from schemas.user import UserCreate
from core.passwords import hash_paswword

def create_user(db: Session, user_data: UserCreate):
    """Create a new user

    Args:
        db (Session): database session
        user_data (UserCreate): user data

    Returns:
        User: new user
    """
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return None
    
    hashed_password = hash_paswword(user_data.password)
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed_password,
        is_active = True,
        role = UserRole(user_data.role)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user