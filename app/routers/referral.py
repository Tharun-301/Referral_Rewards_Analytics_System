from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models import User
from app.schemas import ReferralCodeOut
from app.services import referral_service

router = APIRouter(prefix="/api/referral", tags=["Referral"])


@router.post("/generate", response_model=ReferralCodeOut)
def generate_referral_code(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    code = referral_service.get_or_create_referral_code(db, current_user)
    return {"referral_code": code}