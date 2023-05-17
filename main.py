from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.api.users import users_router

app = FastAPI()


# API Routers
app.include_router(users_router, prefix="/api")


# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
