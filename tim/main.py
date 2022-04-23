from fastapi import FastAPI
from .api.routes import users, items, login

app = FastAPI(title="T.I.M - Triangle Inventory Management")

app.include_router(users.route)
app.include_router(items.route)
app.include_router(login.route)
