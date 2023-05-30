from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.core import settings
from app.api.api_v1.api import api_router
from app.core.init_data import _init_data
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

origins = [
    "http://localhost",
    "http://localhost:5173",  # Replace with the actual origin of your frontend application
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# def init_data():
#     initial_set = _init_data()
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(_init_data, "cron", hour=8)
#     scheduler.start()

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

app.include_router(api_router, prefix=settings.API_V1_STR)
