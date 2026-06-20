from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ReferralCodeOut(BaseModel):
    referral_code: str


class ApplyReferralRequest(BaseModel):
    referral_code: str


class ApplyReferralResponse(BaseModel):
    message: str    

class ReferralSummaryOut(BaseModel):
    my_referral_code: Optional[str]
    total_referrals: int
    successful_referrals: int
    conversion_rate: str


class ReferralListItem(BaseModel):
    used_by_user_id: Optional[str]
    used_at: Optional[datetime]
    status: str


class ReferralTimelineItem(BaseModel):
    date: str
    count: int

class RewardSummaryOut(BaseModel):
    total_earned: int
    pending: int
    credited: int
    unit: Optional[str]


class RewardHistoryItem(BaseModel):
    id: int
    referral_id: int
    reward_type: str
    reward_value: int
    reward_unit: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True