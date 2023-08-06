from datetime import date, time
from fastapi_utils.enums import StrEnum
from pydantic import BaseModel
from typing import Optional

from . import qpu


class DayOfWeek(StrEnum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

    def __str__(self):
        return str(self.value)


class AccessType(StrEnum):
    GROUP = "GROUP"
    ROLE = "ROLE"
    ORG = "ORG"
    QPU = "QPU"

    def __str__(self):
        return str(self.value)


class AccessSlot(BaseModel):
    day: DayOfWeek
    start_date: date
    end_date: Optional[date]
    start_time: time
    end_time: time


class Access(BaseModel):
    qpu_name: qpu.QPUName
    access_name: Optional[str]
    access_type: AccessType
    access_slots: list[AccessSlot] = []
