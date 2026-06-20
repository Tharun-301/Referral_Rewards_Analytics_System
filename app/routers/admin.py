from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import get_current_admin
from app.models import User
from app.schemas import TopReferrerItem, RewardOut
from app.services import referral_service, reward_service

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/referral/top", response_model=List[TopReferrerItem])
def top_referrers(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return referral_service.get_top_referrers(db)


@router.post("/rewards/{reward_id}/credit", response_model=RewardOut)
def credit_reward(
    reward_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return reward_service.credit_reward(db, reward_id)