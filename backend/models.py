"""Module for defining the database models."""

from typing import Any

from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, func
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import validates
from sqlalchemy import event


Base: DeclarativeMeta = declarative_base()

ALLOWED_SALUTATIONS = {"Dr.", "Mr.", "Ms.", "Mrs.", "Mx."}
ALLOWED_GENDERS = {"Male", "Female", "Unspecified"}


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(Integer(), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    full_name = Column(String(255), nullable=False)
    salutation = Column(String(4), nullable=False)
    gender = Column(String(11), nullable=False, default="Unspecified")
    gross_salary: Column[DECIMAL] = Column(DECIMAL(12, 2), nullable=True)
    profile_color = Column(String(7), nullable=False, default="Default")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    @validates("salutation")
    def validate_salutation(self, key: str, value: str) -> str:
        if value not in ["Dr.", "Mr.", "Ms.", "Mrs.", "Mx."]:
            raise ValueError("Invalid salutation.")
        if value == "Mr.":
            self.gender = "Male"
        elif value in ["Mrs.", "Ms."]:
            self.gender = "Female"
        elif value == "Mx.":
            self.gender = "Unspecified"
        return value

    @validates("gender")
    def validate_gender(self, key: str, value: str) -> str:
        if value not in ALLOWED_GENDERS:
            raise ValueError(f"Invalid gender. Must be one of {ALLOWED_GENDERS}")
        return value


@event.listens_for(Employee, "before_insert")
def set_full_name_before_insert(mapper: Any, connection: Any, target: Employee) -> None:
    target.full_name = f"{target.first_name} {target.last_name}".strip()


@event.listens_for(Employee, "before_update")
def set_full_name_before_update(mapper: Any, connection: Any, target: Employee) -> None:
    target.full_name = f"{target.first_name} {target.last_name}".strip()
