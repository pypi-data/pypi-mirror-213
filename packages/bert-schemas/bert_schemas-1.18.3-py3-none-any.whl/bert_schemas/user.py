# type: ignore
from datetime import datetime
from typing import List, Optional, Type

from fastapi_utils.enums import StrEnum
from pydantic import BaseModel, EmailStr, constr

from .questionnaire import RegistrationQandA

external_user_id: Type[str] = constr(regex=r"^auth0|[a-z0-9]{24}$")


class TierName(StrEnum):
    GROUND = "GROUND"
    EXPLORER = "EXPLORER"
    INNOVATOR = "INNOVATOR"
    ADMIN = "ADMIN"

    def __str__(self):
        return str(self.value)


class RoleName(StrEnum):
    SUPERUSER = "SUPERUSER"
    ORG_ADMIN = "ORG_ADMIN"

    def __str__(self):
        return str(self.value)


class JobLimitType(StrEnum):
    JOB_RATE = "JOB_RATE"
    JOB_QUOTA = "JOB_QUOTA"


class ExternalUserId(BaseModel):
    id: external_user_id


class TierBase(BaseModel):
    name: TierName
    description: Optional[str]

    class Config:
        orm_mode = True


class Tier(TierBase):
    pass


class TierCreate(TierBase):
    pass


class RoleBase(BaseModel):
    name: RoleName
    description: Optional[str]

    class Config:
        orm_mode = True


class Role(RoleBase):
    pass


class TierSubscription(BaseModel):
    start_date: datetime
    end_date: datetime = None

    class Config:
        orm_mode = True


class Organization(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    affiliation: str

    class Config:
        orm_mode = True
        extra = "forbid"


class UserResponse(UserBase):
    signup_date: datetime
    external_user_id: external_user_id
    tier: Optional[Tier]
    subscription: Optional[TierSubscription]
    roles: Optional[List[Role]]
    organizations: Optional[List[Organization]]


class User(UserBase):
    id: int
    external_user_id: external_user_id
    signup_date: datetime
    tier: Optional[Tier]
    subscription: Optional[List[TierSubscription]]
    roles: Optional[List[Role]]
    organizations: Optional[List[Organization]]


class UserCreate(UserBase):
    external_user_id: external_user_id


class UserSignUp(UserBase):
    questionnaire: RegistrationQandA
    response: Optional[str]

    class Config:
        use_enum_values = True


class Quota(BaseModel):
    quota_period: str
    quota_limit: Optional[int]
    quota_remaining: Optional[int]


class Rate(BaseModel):
    rate_period: str
    rate_limit: Optional[int]
    rate_remaining: Optional[int]


class JobLimit(BaseModel):
    quotas: List[Quota]
    rates: List[Rate]


class ContactUs(BaseModel):
    subject: str
    email: EmailStr
    content: constr(min_length=1, max_length=500)
