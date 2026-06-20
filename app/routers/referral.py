from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import get_current_user
from app.models import User
from app.schemas import (
    ReferralCodeOut,
    ApplyReferralRequest,
    ApplyReferralResponse,
    ReferralSummaryOut,
    ReferralListItem,
    ReferralTimelineItem,
)
from app.services import referral_service

router = APIRouter(prefix="/api/referral", tags=["Referral"])


@router.post("/generate", response_model=ReferralCodeOut)
def generate_referral_code(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    code = referral_service.get_or_create_referral_code(db, current_user)
    return {"referral_code": code}


@router.post("/apply", response_model=ApplyReferralResponse, status_code=status.HTTP_201_CREATED)
def apply_referral_code(
    payload: ApplyReferralRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    referral_service.apply_referral_code(db, current_user, payload.referral_code)
    return {"message": "Referral applied successfully"}


@router.get("/analytics/summary", response_model=ReferralSummaryOut)
def referral_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return referral_service.get_referral_summary(db, current_user)


@router.get("/analytics/list", response_model=List[ReferralListItem])
def referral_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return referral_service.get_referral_list(db, current_user)


@router.get("/analytics/timeline", response_model=List[ReferralTimelineItem])
def referral_timeline(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return referral_service.get_referral_timeline(db, current_user)