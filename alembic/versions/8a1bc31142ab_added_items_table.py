"""added items table

Revision ID: 8a1bc31142ab
Revises: e82387d4aa0d
Create Date: 2022-04-17 19:55:29.046887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8a1bc31142ab"
down_revision = "e82387d4aa0d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "items",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("title", sa.String, index=True),
        sa.Column("description", sa.String, index=True, default=None),
        sa.Column("bar_code", sa.String, index=True),
        sa.Column("price", sa.DECIMAL(10, 2), index=True),
        sa.Column("image_path", sa.String, default=None),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("items")
