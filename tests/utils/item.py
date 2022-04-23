import random
from typing import Optional
from decimal import Decimal

from sqlalchemy.orm import Session

from tim.db import crud, models
from tim.db.schemas import ItemCreate
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string


def create_random_item(db: Session, *, quantity: Optional[int] = None, owner_id: Optional[int] = None) -> models.Item:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id

    if quantity is None:
        quantity = random.randint(0, 500)

    title = random_lower_string()
    description = random_lower_string()
    bar_code = random_lower_string()
    price = Decimal(round(random.uniform(33.33, 66.66), 2))
    item_in = ItemCreate(title=title, description=description, bar_code=bar_code, price=price, quantity=quantity)
    return crud.create_user_item(db=db, item=item_in, user_id=owner_id)
