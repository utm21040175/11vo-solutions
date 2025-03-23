from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_paswword(password: str) -> str:
    """Encrypt password before saving it in the database

    Args:
        password (str): password to encrypt

    Returns:
        str: encrypted password
    """
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password

    Args:
        plain_password (str): password to verify
        hashed_password (str): password to verify against hashed password

    Returns:
        bool: True if password is correct, False otherwise
    """
    try:
        ph.verify(hashed_password, plain_password)
    except:
        return False
    return True