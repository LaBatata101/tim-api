from decimal import Decimal
from fastapi.encoders import jsonable_encoder
from starlette.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.user import create_random_user
from tim.db.schemas import UserCreate, ItemCreate, Item
from tim.db import crud
from tests.utils.item import create_random_item
from tests.utils.utils import get_user_token_headers


def test_read_items(client: TestClient, db: Session):
    user_in = UserCreate(name="JOHN", email="example@example.com", is_admin=False, password="12345")
    user = crud.create_user(db, user_in)
    item1 = ItemCreate(title="Cookie", bar_code="1293829383949384", description="Biscoito", price=Decimal(2.45))
    item2 = ItemCreate(title="Pizza", bar_code="12829383949384", price=Decimal(22))

    crud.create_user_item(db, item1, user.id)
    crud.create_user_item(db, item2, user.id)

    response = client.get(
        "/items/", headers=get_user_token_headers(client, {"username": user_in.email, "password": user_in.password})
    )
    assert response.status_code == 200
    assert response.json() == [
        Item(**item1.dict(), id=1, owner_id=user.id).dict(),
        Item(**item2.dict(), id=2, owner_id=user.id).dict(),
    ]


def test_read_item_by_title(client: TestClient, db: Session):
    user_in = UserCreate(name="JOHN", email="example@example.com", is_admin=False, password="12345")
    user = crud.create_user(db, user_in)
    item1 = ItemCreate(title="Cookie Cookie", bar_code="1293829383949384", description="Biscoito", price=Decimal(2.45))
    item2 = ItemCreate(title="Pizza", bar_code="12829383949384", price=Decimal(22))

    crud.create_user_item(db, item1, user.id)
    crud.create_user_item(db, item2, user.id)

    response = client.get(
        f"/items/{item1.title}",
        headers=get_user_token_headers(client, {"username": user_in.email, "password": user_in.password}),
    )
    assert response.status_code == 200
    assert response.json() == Item(**item1.dict(), id=1, owner_id=user.id).dict()


def test_update_item(client: TestClient, db: Session):
    user_in = UserCreate(name="JOHN", email="example@example.com", is_admin=False, password="12345")
    user = crud.create_user(db, user_in)
    item1 = ItemCreate(title="Cookie", bar_code="1293829383949384", description="Biscoito", price=Decimal(2.45))

    item1_db = crud.create_user_item(db, item1, user.id)

    response = client.put(
        f"/items/update/{item1_db.id}",
        json={"title": "Pizza", "description": "Made in Italy"},
        headers=get_user_token_headers(client, {"username": user_in.email, "password": user_in.password}),
    )
    assert response.status_code == 200
    assert (
        response.json()
        == Item(
            **item1.dict(exclude={"title", "description"}),
            id=1,
            owner_id=user.id,
            title="Pizza",
            description="Made in Italy",
        ).dict()
    )


def test_delete_item(client: TestClient, db: Session):
    user_in = UserCreate(name="JOHN", email="example@example.com", is_admin=False, password="12345")
    user = crud.create_user(db, user_in)
    item1 = ItemCreate(title="Cookie", bar_code="1293829383949384", description="Biscoito", price=Decimal(2.45))

    item1_db = crud.create_user_item(db, item1, user.id)

    response = client.delete(
        f"/items/delete/{item1_db.id}",
        headers=get_user_token_headers(client, {"username": user_in.email, "password": user_in.password}),
    )
    assert response.status_code == 200

    assert crud.get_item_by_title(db, item1.title) is None


def test_withdraw_item(client: TestClient, db: Session):
    user_in = UserCreate(name="JOHN", email="example@example.com", is_admin=False, password="12345")
    user = crud.create_user(db, user_in)
    item = create_random_item(db, owner_id=user.id, quantity=50)

    response = client.get(
        f"/items/withdraw/{item.id}",
        params={"quantity": 25},
        headers=get_user_token_headers(client, {"username": user_in.email, "password": user_in.password}),
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 25


def test_withdraw_item_with_quantity_less_than_requested(client: TestClient, db: Session):
    user_in = UserCreate(name="JOHN", email="example@example.com", is_admin=False, password="12345")
    user = crud.create_user(db, user_in)
    item = create_random_item(db, owner_id=user.id, quantity=5)

    response = client.get(
        f"/items/withdraw/{item.id}",
        params={"quantity": 25},
        headers=get_user_token_headers(client, {"username": user_in.email, "password": user_in.password}),
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Available item quantity, 5, is less than the requested quantity, 25"}
