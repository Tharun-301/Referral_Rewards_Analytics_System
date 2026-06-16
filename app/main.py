from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Referral & Rewards System")

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "API is running"}