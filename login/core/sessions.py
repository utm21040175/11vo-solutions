from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

serializer = URLSafeTimedSerializer(SECRET_KEY)

def create_session_token(user_id: str):
    """Create session token to authenticate users

    Args:
        user_id (str): user id to include in the token

    Returns:
        str: session token
    """
    return serializer.dumps({"user_id": user_id})

def verify_session_token(token: str, max_age: 3600):
    """Verify if the session token is valid

    Args:
        token (str): token to verify
        max_age (int): max age of the token

    Returns:
        dict: data included in the token
    """
    try:
        return serializer.loads(token, max_age=max_age)
    except:
        return None
