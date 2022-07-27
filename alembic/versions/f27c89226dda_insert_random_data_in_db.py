"""insert random data in db

Revision ID: f27c89226dda
Revises: 8a1bc31142ab
Create Date: 2022-05-22 17:48:37.864635

"""
import sqlalchemy as sa
from faker import Faker
from sqlalchemy import orm

from alembic import op
from tim.db.crud import create_user_item
from tim.models import Item
from tim.schemas import ItemCreate

# revision identifiers, used by Alembic.
revision = "f27c89226dda"
down_revision = "8a1bc31142ab"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    faker = Faker()

    for _ in range(100):
        item = ItemCreate(
            title=faker.name(),
            bar_code=faker.ean13(),
            description=faker.paragraph(),
            price=faker.pydecimal(right_digits=2, min_value=0.0, max_value=1000.0),
            quantity=faker.pyint(),
        )
        create_user_item(session, item, 1)


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.query(Item).delete()
    session.commit()
