import logging
from functools import cache
from logging.handlers import RotatingFileHandler

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class DbSettings(BaseSettings):
    DB_URL: str
    DB_URL_SYNC: str

    PAGINATION_LIMIT: int = 50


class LoggingSettings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = "app.log"

    class Config:
        env_prefix = "LOG_"


class APISettings(BaseSettings):
    SENTIMENT_ANALYSIS_BASE_URL: str
    SENTIMENT_ANALYSIS_API_KEY: str

    IP_API_BASE_URL: str


def setup_logger() -> logging.Logger:
    settings = LoggingSettings()
    logger = logging.getLogger("app")
    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(settings.LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if settings.LOG_FILE:
        log_path = Path(settings.LOG_FILE)
        log_path.parent.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            log_path, mode="w", encoding="utf-8",
            maxBytes=5*1024*1024, backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


@cache
def get_db_settings() -> DbSettings:
    return DbSettings()


@cache
def get_api_settings() -> APISettings:
    return APISettings()


logger = setup_logger()
db_settings = get_db_settings()
api_settings = get_api_settings()
