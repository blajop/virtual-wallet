from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi_pagination import add_pagination
import uvicorn

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
    "https://uncles.vercel.app",
    "http://localhost",
    "http://localhost:5173",
    "http://91.139.226.224:80",  # Replace with the actual origin of your frontend application
    "http://91.139.226.224",  # Replace with the actual origin of your frontend application
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

add_pagination(app)

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=443, reload=True)
