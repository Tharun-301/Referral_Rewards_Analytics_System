import random
import string
from sqlalchemy.orm import Session
from app.models import RewardConfig, RewardLedger, Referral, User
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import func
from app.services import reward_service


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
    owner_referral = (
        db.query(Referral)
        .filter(Referral.referral_code == code, Referral.referral_code_used.is_(None))
        .first()
    )
    if not owner_referral:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid referral code")

    if owner_referral.referred_by == applying_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot refer yourself")

    already_used = (
        db.query(Referral)
        .filter(Referral.referral_code_used == applying_user.id)
        .first()
    )
    if already_used:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Code already used")

    usage = Referral(
        referral_code=code,
        referred_by=owner_referral.referred_by,
        referral_code_used=applying_user.id,
        referral_used_at=datetime.utcnow(),
    )
    db.add(usage)
    db.commit()
    db.refresh(usage)


    reward_service.create_pending_reward_for_referral(db, usage)

    return usage



def get_referral_summary(db: Session, user: User) -> dict:
    my_code_row = (
        db.query(Referral)
        .filter(Referral.referred_by == user.id, Referral.referral_code_used.is_(None))
        .first()
    )
    my_code = my_code_row.referral_code if my_code_row else None

    total = db.query(func.count(Referral.id)).filter(Referral.referred_by == user.id).scalar()
    successful = (
        db.query(func.count(Referral.id))
        .filter(Referral.referred_by == user.id, Referral.referral_code_used.isnot(None))
        .scalar()
    )

    conversion_rate = f"{round((successful / total) * 100)}%" if total else "0%"

    return {
        "my_referral_code": my_code,
        "total_referrals": total,
        "successful_referrals": successful,
        "conversion_rate": conversion_rate,
    }


def get_referral_list(db: Session, user: User) -> list[dict]:
    rows = (
        db.query(Referral)
        .filter(Referral.referred_by == user.id)
        .order_by(Referral.referred_at.desc())
        .all()
    )
    return [
        {
            "used_by_user_id": r.referral_code_used,
            "used_at": r.referral_used_at,
            "status": "SUCCESS" if r.referral_code_used else "PENDING",
        }
        for r in rows
    ]


def get_referral_timeline(db: Session, user: User) -> list[dict]:
    rows = (
        db.query(
            func.date(Referral.referral_used_at).label("date"),
            func.count(Referral.id).label("count"),
        )
        .filter(Referral.referred_by == user.id, Referral.referral_code_used.isnot(None))
        .group_by(func.date(Referral.referral_used_at))
        .order_by(func.date(Referral.referral_used_at))
        .all()
    )
    return [{"date": str(r.date), "count": r.count} for r in rows]

def get_top_referrers(db: Session, limit: int = 10) -> list[dict]:
    rows = (
        db.query(
            Referral.referred_by.label("user_id"),
            func.count(Referral.id).label("successful_referrals"),
        )
        .filter(Referral.referral_code_used.isnot(None))
        .group_by(Referral.referred_by)
        .order_by(func.count(Referral.id).desc())
        .limit(limit)
        .all()
    )
    return [{"user_id": r.user_id, "successful_referrals": r.successful_referrals} for r in rows]