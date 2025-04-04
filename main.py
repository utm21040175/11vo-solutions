from fastapi import FastAPI
from login.routes import user
from products.routes import products, cart
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="11vo Solutions API", version="0.1.0")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app.include_router(user.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])

@app.get("/")
def root():
    return {"message": "Welcome to 11vo Solutions API"}