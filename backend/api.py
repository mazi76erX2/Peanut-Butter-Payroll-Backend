"""
API router module for employee endpoints.
This module imports CRUD functions, Pydantic schemas, and uses the async
session dependency from database.py.
"""

import logging

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Any

from schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from crud import (
    create_employee,
    delete_employee,
    get_employee,
    get_employees,
    update_employee,
)
from database import get_session

from faker import Faker

router: APIRouter = APIRouter(prefix="/api/employees", tags=["employees"])
logger = logging.getLogger(__name__)
fake: Faker = Faker()


@router.get("/", response_model=List[EmployeeResponse])
async def list_employees(
    search: Optional[str] = Query(None, min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_session),
) -> List[EmployeeResponse]:
    skip: int = (page - 1) * page_size
    employees = await get_employees(db, skip=skip, limit=page_size, search=search)
    return employees


@router.post("/", response_model=EmployeeResponse)
async def create_employee_endpoint(
    employee: EmployeeCreate, db: AsyncSession = Depends(get_session)
) -> EmployeeResponse:
    try:
        new_employee = await create_employee(db, employee)
        return new_employee
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee_endpoint(
    employee_id: int, db: AsyncSession = Depends(get_session)
) -> EmployeeResponse:
    db_employee = await get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee_endpoint(
    employee_id: int, employee: EmployeeUpdate, db: AsyncSession = Depends(get_session)
) -> EmployeeResponse:
    db_employee = await get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    try:
        updated_employee = await update_employee(db, db_employee, employee)
        return updated_employee
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{employee_id}")
async def delete_employee_endpoint(
    employee_id: int, db: AsyncSession = Depends(get_session)
) -> dict:
    db_employee = await get_employee(db, employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    await delete_employee(db, db_employee)
    return {"status": "success", "message": "Employee deleted"}


@router.post("/seed", response_model=dict)
async def seed_data_endpoint(db: AsyncSession = Depends(get_session)) -> dict:
    """
    Seed the database with default employee data using Faker.
    This endpoint inserts 10 new employee records.
    """
    count: int = 0
    for _ in range(10):
        data: dict[str, Any] = {
            "employee_number": str(fake.random_number(digits=5, fix_len=True)),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "salutation": fake.random_element(
                elements=("Mr.", "Mrs.", "Ms.", "Dr.", "Mx.")
            ),
            "gender": "Unspecified",
            "gross_salary": fake.random_int(min=30000, max=100000),
            "profile_color": fake.random_element(
                elements=("Default", "Green", "Blue", "Red")
            ),
        }
        employee_data = EmployeeCreate(**data)
        try:
            await create_employee(db, employee_data)
            count += 1
            logger.info(f"Seeded employee {data['employee_number']}")
        except Exception as e:
            logger.error(f"Error seeding employee {data.get('employee_number')}: {e}")
    return {"status": "success", "message": f"Seeded {count} employees."}
