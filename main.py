from fastapi import FastAPI
from login.routes import user

app = FastAPI(title="11vo Solutions API", version="0.1.0")

app.include_router(user.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Welcome to 11vo Solutions API"}