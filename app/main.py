from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.auth import router as auth_router
from app.routers.referral import router as referral_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Referral & Rewards System")

app.include_router(auth_router)
app.include_router(referral_router)


@app.get("/")
def root():
    return {"message": "API is running"}