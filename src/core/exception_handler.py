from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.core.exceptions import AppException


async def app_exception_handler(
        request: Request,
        exception: AppException,
) -> JSONResponse:
    """
    Custom exceptions handler.
    :param request: Request object.
    :param exception: Custom exception object.
    :return: JSONResponse object.
    """
    return JSONResponse(
        status_code=exception.code,
        content={
            "message": exception.message,
            "details": exception.details or "No additional details"
        }
    )
