from authlib.jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

JWT_CONFIG = {
    "alg": "H256"
}

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