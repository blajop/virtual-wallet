from app.api.api_v1.endpoints import wallets, users, transactions, login, cards
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter


api_router = APIRouter()

api_router.include_router(login.router, tags=["00. API / Login"])
users.router.include_router(wallets.router, prefix="/{identifier}/wallets")
api_router.include_router(users.router, prefix="/users", tags=["01. API / Users"])
api_router.include_router(cards.router, prefix="/cards", tags=["02. API / Cards"])
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["03. API / Transactions"]
)
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
