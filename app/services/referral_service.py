import random
import string
from sqlalchemy.orm import Session
from app.models import Referral, User
from datetime import datetime
from fastapi import HTTPException, status


def _generate_code() -> str:
    suffix = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )
    return f"SVH-{suffix}"


def get_or_create_referral_code(db: Session, user: User) -> str:
    existing = (
        db.query(Referral)
        .filter(Referral.referred_by == user.id)
        .first()
    )

    if existing:
        return existing.referral_code

    for _ in range(5):
        code = _generate_code()

        clash = (
            db.query(Referral)
            .filter(Referral.referral_code == code)
            .first()
        )

        if not clash:
            referral = Referral(
                referral_code=code,
                referred_by=user.id
            )

            db.add(referral)
            db.commit()
            db.refresh(referral)

            return referral.referral_code

    raise RuntimeError("Could not generate a unique referral code, try again")

def apply_referral_code(db: Session, applying_user: User, code: str) -> Referral:
    # 1. Find the code's "definition" row — the owner's original generated code
    owner_referral = (
        db.query(Referral)
        .filter(Referral.referral_code == code, Referral.referral_code_used.is_(None))
        .first()
    )
    if not owner_referral:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid referral code")

    # 2. Block self-referral
    if owner_referral.referred_by == applying_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot refer yourself")

    # 3. Block a user from applying ANY referral code more than once
    #    (this also covers "same code reused by same user" automatically)
    already_used = (
        db.query(Referral)
        .filter(Referral.referral_code_used == applying_user.id)
        .first()
    )
    if already_used:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Code already used")

    # 4. Record this usage as a brand-new row
    usage = Referral(
        referral_code=code,
        referred_by=owner_referral.referred_by,
        referral_code_used=applying_user.id,
        referral_used_at=datetime.utcnow(),
    )
    db.add(usage)
    db.commit()
    db.refresh(usage)
    return usage