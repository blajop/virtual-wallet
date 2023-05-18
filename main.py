from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.api_v1.endpoints.users import router
from app.api.api_v1.endpoints.wallets import wallets_router

app = FastAPI()


# API Routers
app.include_router(router, prefix="/api")
app.include_router(wallets_router, prefix="/api")


# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
