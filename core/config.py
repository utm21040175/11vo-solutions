from dotenv import load_dotenv
import os

load_dotenv()

class Settings():
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    
settings = Settings()