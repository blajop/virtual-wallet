from fastapi import APIRouter
from app.api.api_v1.endpoints import wallets, users, transactions, login
from fastapi.staticfiles import StaticFiles


api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["01. API / Users"])
api_router.include_router(wallets.router, prefix="/wallets", tags=["02. API / Wallets"])
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["03. API / Transactions"]
)
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
