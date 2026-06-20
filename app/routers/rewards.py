from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import get_current_user
from app.models import User
from app.schemas import RewardSummaryOut, RewardHistoryItem
from app.services import reward_service

router = APIRouter(prefix="/api/rewards", tags=["Rewards"])


@router.get("/summary", response_model=RewardSummaryOut)
def reward_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return reward_service.get_reward_summary(db, current_user)


@router.get("/history", response_model=List[RewardHistoryItem])
def reward_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return reward_service.get_reward_history(db, current_user)