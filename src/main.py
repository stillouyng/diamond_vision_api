from fastapi import FastAPI, Request

from src.api import complaints_router
from src.core.config import logger
from src.core.exception_handler import app_exception_handler
from src.core.exceptions import AppException

app = FastAPI()

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(
    complaints_router,
    prefix="/api/v1/complaints",
    tags=["complaints"]
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Request handler middleware for logging requests.
    :param request: Request object.
    :param call_next: Call next middleware.
    :return: None
    """
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
