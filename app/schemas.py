from pydantic import BaseModel
from datetime import datetime


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