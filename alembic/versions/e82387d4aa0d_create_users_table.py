"""create users table

Revision ID: e82387d4aa0d
Revises: 
Create Date: 2022-04-17 19:41:24.452031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e82387d4aa0d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, index=True, nullable=False),
        sa.Column("email", sa.String, index=True, unique=True, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_admin", sa.Boolean, default=False),
    )


def downgrade():
    op.drop_table("users")
