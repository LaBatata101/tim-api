import random
import string
from typing import Dict

from fastapi.testclient import TestClient


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_numbers_string() -> str:
    return "".join(random.choices(string.digits, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_user_token_headers(client: TestClient, login_data: Dict[str, str]) -> Dict[str, str]:
    r = client.post(f"/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
