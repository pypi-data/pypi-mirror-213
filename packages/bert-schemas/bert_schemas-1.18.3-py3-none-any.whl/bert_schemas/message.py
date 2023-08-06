from datetime import datetime
from typing import Union

from pydantic import BaseModel, validator


class MessageBase(BaseModel):
    location: int = 1
    message: str
    start_datetime: datetime
    end_datetime: datetime

    class Config:
        orm_mode = True
        validate_assignment = True


class Message(MessageBase):
    id: int


class MessageResponse(Message):
    location: int = 1
    message: str
    start_datetime: Union[str, datetime]
    end_datetime: Union[str, datetime]

    @validator("start_datetime", pre=True)
    def formate_start_datetime(cls, value):
        return value.strftime("%m/%d/%Y @ %H:%M")

    @validator("end_datetime", pre=True)
    def formate_end_datetime(cls, value):
        return value.strftime("%m/%d/%Y @ %H:%M")
