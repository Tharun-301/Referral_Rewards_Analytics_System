from fastapi import FastAPI
from app.database import engine, Base, SessionLocal
from app import models
from app.auth import router as auth_router
from app.routers.referral import router as referral_router
from app.routers.rewards import router as rewards_router
from app.services.reward_service import seed_default_reward_config

Base.metadata.create_all(bind=engine)

# Seed one default reward config if none exists (dev convenience, not hardcoded business logic)
db = SessionLocal()
try:
    seed_default_reward_config(db)
finally:
    db.close()

app = FastAPI(title="Referral & Rewards System")

app.include_router(auth_router)
app.include_router(referral_router)
app.include_router(rewards_router)


@app.get("/")
def root():
    return {"message": "API is running"}