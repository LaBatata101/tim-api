from tim.db import crud
from tim.db.schemas import ItemCreate, ItemUpdate
from decimal import Decimal
from sqlalchemy.orm import Session
from tests.utils.user import create_random_user
from tests.utils.item import create_random_item
from tests.utils.utils import random_lower_string, random_numbers_string


def test_create_item(db: Session):
    user_db = create_random_user(db)

    title = random_lower_string()
    bar_code = random_numbers_string()

    item = ItemCreate(title=title, bar_code=bar_code, price=Decimal(25.5), quantity=5)
    item_db = crud.create_user_item(db, item, user_db.id)

    assert item_db.title == title
    assert item_db.bar_code == bar_code
    assert item_db.quantity == 5
    assert item_db.price == Decimal(25.5)
    assert item_db.owner_id == user_db.id


def test_delete_item(db: Session):
    item_db = create_random_item(db)

    deleted_item = crud.delete_item(db, id=item_db.id)
    assert deleted_item


def test_update_item(db: Session):
    item_db = create_random_item(db)

    updated_item = crud.update_item(db, item_db, ItemUpdate(title="Cookies"))

    assert updated_item.title == "Cookies"


def test_get_item(db: Session):
    item = create_random_item(db)

    item_db = crud.get_item_by_title(db, item.title)
    assert item_db
    assert item_db.title == item.title
    assert item_db.bar_code == item.bar_code
