from sqlalchemy import create_engine
from app.core import settings

engine = create_engine(settings.DB_ENGINE_URI, pool_pre_ping=True)
