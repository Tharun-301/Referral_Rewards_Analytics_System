from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import RewardConfig, RewardLedger, Referral, User


def seed_default_reward_config(db: Session):
    """Creates one default SIGNUP reward config if none exists yet. Dev convenience only."""
    existing = db.query(RewardConfig).filter(RewardConfig.reward_type == "SIGNUP").first()
    if not existing:
        config = RewardConfig(
            reward_type="SIGNUP",
            reward_value=100,
            reward_unit="POINTS",
            is_active=True,
        )
        db.add(config)
        db.commit()


def create_pending_reward_for_referral(db: Session, referral: Referral) -> RewardLedger | None:
    """
    Called right after a referral is successfully applied.
    Creates a PENDING reward for the REFERRER (the code owner), using
    whatever value/unit is currently configured — never a hardcoded number.
    """
    # Idempotency guard: never create two rewards for the same referral
    existing = db.query(RewardLedger).filter(RewardLedger.referral_id == referral.id).first()
    if existing:
        return existing

    config = (
        db.query(RewardConfig)
        .filter(RewardConfig.reward_type == "SIGNUP", RewardConfig.is_active.is_(True))
        .first()
    )
    if not config:
        return None  # no active reward configured — referral still succeeds, just no reward

    ledger_entry = RewardLedger(
        user_id=referral.referred_by,
        referral_id=referral.id,
        reward_type=config.reward_type,
        reward_value=config.reward_value,
        reward_unit=config.reward_unit,
        status="PENDING",
    )
    db.add(ledger_entry)
    db.commit()
    db.refresh(ledger_entry)
    return ledger_entry


def get_reward_summary(db: Session, user: User) -> dict:
    pending = (
        db.query(func.coalesce(func.sum(RewardLedger.reward_value), 0))
        .filter(RewardLedger.user_id == user.id, RewardLedger.status == "PENDING")
        .scalar()
    )
    credited = (
        db.query(func.coalesce(func.sum(RewardLedger.reward_value), 0))
        .filter(RewardLedger.user_id == user.id, RewardLedger.status == "CREDITED")
        .scalar()
    )
    unit_row = db.query(RewardLedger.reward_unit).filter(RewardLedger.user_id == user.id).first()

    return {
        "total_earned": credited,   # "earned" = actually credited, not just promised
        "pending": pending,
        "credited": credited,
        "unit": unit_row[0] if unit_row else None,
    }


def get_reward_history(db: Session, user: User) -> list[RewardLedger]:
    return (
        db.query(RewardLedger)
        .filter(RewardLedger.user_id == user.id)
        .order_by(RewardLedger.created_at.desc())
        .all()
    )