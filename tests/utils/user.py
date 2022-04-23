from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tim.db import crud
from tim.db.models import User
from tim.db.schemas import UserCreate
from tests.utils.utils import random_email, random_lower_string


def create_random_user(db: Session, is_admin: bool = False) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(name=email, email=email, password=password, is_admin=is_admin)
    user = crud.create_user(db=db, user=user_in)
    return user
