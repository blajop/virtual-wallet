from fastapi import FastAPI
from app.core.config import settings
from app.api.api_v1.api import api_router
from apscheduler.schedulers.background import BackgroundScheduler
from app.core.init_data import _init_data


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


# @app.on_event("startup")
# def init_data():
#     initial_set = _init_data()
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(_init_data, "cron", hour=8)
#     scheduler.start()


app.include_router(api_router, prefix=settings.API_V1_STR)
