from decimal import Decimal
from fastapi.encoders import jsonable_encoder
from starlette.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.user import create_random_user
from tests.utils.utils import get_user_token_headers
from tim.api import security
from tim.db.schemas import User, UserCreate, ItemCreate, Item
from tim.db import crud


def test_create_new_user(client: TestClient):
    user = UserCreate(name="JOHN", email="example@example.com", is_admin=True, password="12345")
    response = client.post("/users/register", json=user.dict())

    assert response.status_code == 201
    assert response.json() == User(**user.dict(), id=1).dict()


def test_create_new_user_with_existing_email(client: TestClient, db: Session):
    crud.create_user(db, UserCreate(name="JOHN", email="example@example.com", is_admin=True, password="12345"))

    user = UserCreate(name="JOHN2", email="example@example.com", is_admin=False, password="12345")
    response = client.post("/users/register", json=user.dict())

    assert response.status_code == 400


def test_login(client: TestClient, db: Session):
    crud.create_user(db, UserCreate(name="admin", email="admin@admin.com", is_admin=True, password="admin"))

    response = client.post("/login/access-token", data={"username": "admin@admin.com", "password": "admin"})
    assert response.status_code == 200
    assert response.json() == {
        "access_token": security.create_access_token(data={"sub": "admin@admin.com"}),
        "token_type": "bearer",
    }


def test_read_user_me(client: TestClient, db: Session):
    user_db = crud.create_user(db, UserCreate(name="admin", email="admin@admin.com", is_admin=True, password="admin"))

    response = client.post("/login/access-token", data={"username": "admin@admin.com", "password": "admin"})
    assert response.status_code == 200

    access_token = response.json()["access_token"]
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json() == User.from_orm(user_db)


def test_update_user(client: TestClient, db: Session):
    user_in = UserCreate(name="admin", email="admin@admin.com", is_admin=True, password="admin")
    user_db = crud.create_user(db, user_in)

    response = client.put(
        f"/users/update/{user_db.id}",
        headers=get_user_token_headers(client, {"username": user_in.email, "password": user_in.password}),
        json={"email": "admin@admin.org", "password": "admin1234"},
    )
    assert response.status_code == 200
    assert response.json() == User.from_orm(user_db)


def test_non_admin_user_update_user(client: TestClient, db: Session):
    user = UserCreate(name="fakeadmin", email="fakeadmin@admin.com", is_admin=False, password="admin")
    crud.create_user(db, user)

    response = client.put(
        "/users/update/1",
        headers=get_user_token_headers(client, {"username": user.email, "password": user.password}),
        json={"email": "admin@admin.org", "password": "admin1234"},
    )

    assert response.status_code == 400


def test_delete_user(client: TestClient, db: Session):
    user = UserCreate(name="admin", email="admin@admin.com", is_admin=True, password="admin")
    crud.create_user(db, user)

    response = client.delete(
        "/users/delete/1",
        headers=get_user_token_headers(client, {"username": user.email, "password": user.password}),
    )

    assert response.status_code == 200
    assert response.json() == {
        "name": "admin",
        "email": "admin@admin.com",
        "is_admin": True,
        "id": 1,
        "items": [],
    }

    user_db = crud.get_user_by_name(db, "name")
    assert user_db is None


def test_read_users(client: TestClient, db: Session):
    user2_in = UserCreate(name="John", email="John@email.com", is_admin=False, password="1234567890")
    user1 = crud.create_user(db, UserCreate(name="admin", email="admin@admin.com", is_admin=True, password="admin"))
    user2 = crud.create_user(db, user2_in)

    response = client.get(
        "/users/",
        headers=get_user_token_headers(client, {"username": user2_in.email, "password": user2_in.password}),
    )
    assert response.status_code == 200
    assert response.json() == [User.from_orm(user1).dict(), User.from_orm(user2).dict()]


def test_create_item_for_user(client: TestClient, db: Session):
    user_in = UserCreate(name="admin", email="admin@admin.com", is_admin=True, password="admin")
    user = crud.create_user(db, user_in)
    item = ItemCreate(title="Cookie", bar_code="1293829383949384", description="Biscoito", price=Decimal(2.45))

    response = client.post(
        f"/users/{user.id}/items/",
        json=jsonable_encoder(item),
        headers=get_user_token_headers(client, {"username": user_in.email, "password": user_in.password}),
    )
    assert response.status_code == 201
    assert response.json() == Item(**item.dict(), id=1, owner_id=user.id)

    user_db = crud.get_user(db, user.id)
    assert len(user_db.items) >= 1
