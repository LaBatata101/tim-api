"""added owner_id column to items table

Revision ID: 258b58f231d2
Revises: 8a1bc31142ab
Create Date: 2022-04-17 20:08:21.478260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "258b58f231d2"
down_revision = "8a1bc31142ab"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("items", sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id")))


def downgrade():
    op.drop_column("items", "owner_id")
