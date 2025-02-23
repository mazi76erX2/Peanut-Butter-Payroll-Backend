"""create employees table

Revision ID: eee1271709d2
Revises: 
Create Date: 2025-02-22 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from typing import Union, Sequence

# revision identifiers, used by Alembic.
revision = "eee1271709d2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("employee_number", sa.Integer(), nullable=False, unique=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("salutation", sa.String(length=4), nullable=False),
        sa.Column(
            "gender", sa.String(length=11), nullable=False, server_default="Unspecified"
        ),
        sa.Column("gross_salary", sa.DECIMAL(12, 2), nullable=True),
        sa.Column(
            "profile_color",
            sa.String(length=7),
            nullable=False,
            server_default="Default",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_employees_employee_number", "employees", ["employee_number"])


def downgrade() -> None:
    op.drop_index("ix_employees_employee_number", table_name="employees")
    op.drop_table("employees")
