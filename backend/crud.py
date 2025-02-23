from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from models import Employee
from schemas import EmployeeCreate, EmployeeUpdate


async def get_employee(db: AsyncSession, employee_id: int) -> Optional[Employee]:
    result = await db.execute(
        select(Employee).where(Employee.id == employee_id)
    )
    return result.scalar_one_or_none()


async def get_employees(
    db: AsyncSession, skip: int = 0, limit: int = 10, search: Optional[str] = None
) -> List[Employee]:
    stmt = select(Employee)
    if search:
        like_pattern = f"%{search}%"
        stmt = stmt.where(
            Employee.first_name.ilike(like_pattern)
            | Employee.last_name.ilike(like_pattern)
            | Employee.employee_number.ilike(like_pattern)
        )
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_employee(
    db: AsyncSession, employee: EmployeeCreate
) -> Employee:
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee


async def update_employee(
    db: AsyncSession, db_employee: Employee, employee: EmployeeUpdate
) -> Employee:
    for key, value in employee.model_dump().items():
        setattr(db_employee, key, value)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee


async def delete_employee(db: AsyncSession, db_employee: Employee) -> None:
    await db.delete(db_employee)
    await db.commit()
