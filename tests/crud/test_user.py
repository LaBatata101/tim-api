from tim.db import crud
from tim.api import security
from sqlalchemy.orm import Session
from tim.db.schemas import UserCreate, UserUpdate
from fastapi.encoders import jsonable_encoder
from tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, name=email, is_admin=False, password=password)
    user = crud.create_user(db, user_in)

    assert user.email == email
    assert user.name == email
    assert hasattr(user, "hashed_password")
    assert user.hashed_password


def test_authenticate_user(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(name=email, email=email, password=password)
    user = crud.create_user(db, user_in)
    authenticated_user = security.authenticate_user(db, email=email, password=password)

    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session):
    email = random_email()
    password = random_lower_string()
    user = security.authenticate_user(db, email=email, password=password)

    assert user is False


def test_get_user(db: Session):
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(name=email, email=email, password=password)
    user = crud.create_user(db, user_in)
    user_2 = crud.get_user(db, user.id)

    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session):
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(name=email, email=email, password=password)
    user = crud.create_user(db, user_in)
    user_db = crud.get_user(db, user.id)

    assert user_db

    update_user = UserUpdate(name="Fool")
    user_updated = crud.update_user(db, user_db, update_user)

    user_db = crud.get_user(db, user_updated.id)

    assert user_db
    assert user_db.name == update_user.name


def test_delete_user(db: Session):
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(name=email, email=email, password=password)
    user = crud.create_user(db, user_in)
    user_db = crud.get_user(db, user.id)

    assert user_db

    deleted_user = crud.delete_user(db, id=user_db.id)
    assert deleted_user == user_db

    user_db = crud.get_user(db, deleted_user.id)
    assert user_db is None


def test_delete_nonexistent_user(db: Session):
    deleted_user = crud.delete_user(db, id=24)
    assert deleted_user is None
