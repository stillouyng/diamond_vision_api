from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker,
    AsyncSession, AsyncEngine
)
from sqlalchemy.orm import declarative_base

from src.core.config import db_settings


database_url = str(db_settings.DB_URL)

engine: AsyncEngine = create_async_engine(
    database_url,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()
