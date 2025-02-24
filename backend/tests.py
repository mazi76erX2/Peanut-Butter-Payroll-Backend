import pytest
import asyncio
from fastapi.testclient import TestClient
from .main import app
from .models import Base
from .database import engine


def create_tables() -> None:
    asyncio.run(_create_tables())


async def _create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def drop_tables() -> None:
    asyncio.run(_drop_tables())


async def _drop_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
def prepare_database() -> None:
    create_tables()
    yield
    drop_tables()


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def test_create_employee(client: TestClient):
    payload = {
        "employee_number": "12345",
        "first_name": "Alice",
        "last_name": "Anderson",
        "salutation": "Ms.",
        "gender": "Female",
        "gross_salary": 55000,
        "profile_color": "Blue",
    }
    response = client.post("/api/employees/", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["employee_number"] == "12345"
    assert data["full_name"] == "Alice Anderson"


def test_list_employees(client: TestClient):
    response = client.get("/api/employees/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_employee(client: TestClient):
    payload = {
        "employee_number": "54321",
        "first_name": "Jane",
        "last_name": "Doe",
        "salutation": "Ms.",
        "gender": "Female",
        "gross_salary": 60000,
        "profile_color": "Red",
    }
    create_response = client.post("/api/employees/", json=payload)
    assert create_response.status_code == 200, create_response.text
    created_data = create_response.json()
    emp_id = created_data["id"]

    update_payload = {
        "employee_number": "54321",
        "first_name": "Janet",
        "last_name": "Smith",
        "salutation": "Ms.",
        "gender": "Female",
        "gross_salary": 65000,
        "profile_color": "Blue",
    }
    update_response = client.put(f"/api/employees/{emp_id}", json=update_payload)
    assert update_response.status_code == 200, update_response.text
    updated_data = update_response.json()
    assert updated_data["first_name"] == "Janet"
    assert updated_data["last_name"] == "Smith"
    assert updated_data["full_name"] == "Janet Smith"


def test_delete_employee(client: TestClient):
    payload = {
        "employee_number": "67890",
        "first_name": "Alice",
        "last_name": "Wonder",
        "salutation": "Dr.",
        "gender": "Female",
        "gross_salary": 70000,
        "profile_color": "Green",
    }
    create_response = client.post("/api/employees/", json=payload)
    assert create_response.status_code == 200, create_response.text
    created_data = create_response.json()
    emp_id = created_data["id"]

    delete_response = client.delete(f"/api/employees/{emp_id}")
    assert delete_response.status_code == 200, delete_response.text

    get_response = client.get(f"/api/employees/{emp_id}")
    assert get_response.status_code == 404


def test_seed_endpoint(client: TestClient):
    seed_response = client.post("/api/employees/seed")
    assert seed_response.status_code == 200, seed_response.text
    seed_data = seed_response.json()
    assert "Seeded" in seed_data.get("message", "")
