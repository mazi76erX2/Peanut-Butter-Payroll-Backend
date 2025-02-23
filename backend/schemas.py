""" Pydantic schemas for the Employee model. """

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from enum import Enum


class SalutationEnum(str, Enum):
    Dr = "Dr."
    Mr = "Mr."
    Ms = "Ms."
    Mrs = "Mrs."
    Mx = "Mx."


class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"
    Unspecified = "Unspecified"


class EmployeeBase(BaseModel):
    employee_number: int
    first_name: str
    last_name: str
    salutation: SalutationEnum
    gender: GenderEnum
    gross_salary: Optional[Decimal] = None
    profile_color: str = "Default"


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int
    full_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
