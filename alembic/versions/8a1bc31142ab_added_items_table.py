"""added items table

Revision ID: 8a1bc31142ab
Revises: e82387d4aa0d
Create Date: 2022-04-17 19:55:29.046887

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "8a1bc31142ab"
down_revision = "e82387d4aa0d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "items",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("title", sa.String(100), index=True),
        sa.Column("description", sa.String(240), index=True, default=None),
        sa.Column("bar_code", sa.String(13), index=True),
        sa.Column("price", sa.DECIMAL(10, 2), index=True),
        sa.Column("quantity", sa.Integer, default=0),
        sa.Column("image_path", sa.String, default=None),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("items")
