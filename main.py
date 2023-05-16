from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
