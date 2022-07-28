"""create users table

Revision ID: e82387d4aa0d
Revises: 
Create Date: 2022-04-17 19:41:24.452031

"""
import sqlalchemy as sa
from sqlalchemy import orm

from alembic import op
from tim.db.crud import create_user
from tim.schemas import UserCreate

# revision identifiers, used by Alembic.
revision = "e82387d4aa0d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(100), index=True, nullable=False),
        sa.Column("email", sa.String(100), index=True, unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(60), nullable=False),
        sa.Column("is_admin", sa.Boolean, default=False),
    )
    create_user(session, UserCreate(name="admin", email="admin@admin.com", is_admin=True, password="admin"))


def downgrade():
    op.drop_table("users")
