import random
import string
from sqlalchemy.orm import Session
from app.models import Referral, User


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