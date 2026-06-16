from fastapi import FastAPI
from app.database import engine, Base
from app import models  # this import matters — it registers the tables

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Referral & Rewards System")

@app.get("/")
def root():
    return {"message": "API is running"}