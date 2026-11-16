import os
from src.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(settings.account_service_database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()