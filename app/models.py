import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from app.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    referral_code = Column(String, nullable=False, index=True)
    referred_by = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    referred_at = Column(DateTime, default=datetime.utcnow)
    referral_code_used = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    referral_used_at = Column(DateTime, nullable=True)


class RewardConfig(Base):
    __tablename__ = "reward_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reward_type = Column(String, nullable=False)     # e.g. 'SIGNUP', 'FIRST_ORDER'
    reward_value = Column(Integer, nullable=False)
    reward_unit = Column(String, nullable=False)      # e.g. 'POINTS', 'CASH'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class RewardLedger(Base):
    __tablename__ = "reward_ledgers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    referral_id = Column(Integer, ForeignKey("referrals.id"), nullable=False)
    reward_type = Column(String, nullable=False)
    reward_value = Column(Integer, nullable=False)
    reward_unit = Column(String, nullable=False)
    status = Column(String, default="PENDING")        # PENDING, CREDITED, REVOKED
    created_at = Column(DateTime, default=datetime.utcnow)