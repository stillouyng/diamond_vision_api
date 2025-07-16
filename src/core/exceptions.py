from fastapi import status

from typing import Any, Optional


class AppException(Exception):
    """
    Base exception class.
    """
    def __init__(
            self,
            message: str,
            code: int,
            details: Optional[Any] = None
    ):
        self.message = message
        self.code = code
        self.details = details


class NotFoundException(AppException):
    """
    Object was not found (404).
    """
    def __init__(
            self,
            message: str = "Object was not found.",
            details: Optional[str] = None
    ):
        super().__init__(
            message, status.HTTP_404_NOT_FOUND, details
        )


class ValidationException(AppException):
    """
    Validation exception class (422).
    """
    def __init__(
            self,
            message: str = "Incorrect input.",
            details: Optional[str] = None
    ):
        super().__init__(
            message, status.HTTP_422_UNPROCESSABLE_ENTITY, details
        )


class IternalException(AppException):
    """
    Iternal Exception class.
    """
    def __init__(
            self,
            message: str = "Internal error.",
            details: Optional[str] = None
    ):
        super().__init__(
            message, status.HTTP_500_INTERNAL_SERVER_ERROR, details
        )


class DatabaseNotFound(AppException):
    """
    Database not found error class.
    """
    def __init__(
            self,
            message: str = "Database not found.",
            details: Optional[str] = "Make sure database is available via "
                                     "'./instance/database.sqlite'"
    ):
        super().__init__(
            message, status.HTTP_500_INTERNAL_SERVER_ERROR, details
        )


class RepositoryError(AppException):
    """
    Repository error class.
    """
    def __init__(
            self,
            message: str,
            details: Optional[str] = None
    ):
        super().__init__(
            message, status.HTTP_500_INTERNAL_SERVER_ERROR, details
        )


class ServiceError(AppException):
    """
    Service error class.
    """
    def __init__(
            self,
            message: str,
            details: Optional[str] = None
    ):
        super().__init__(
            message, status.HTTP_500_INTERNAL_SERVER_ERROR, details
        )


class ComplaintNotFound(AppException):
    """
    Complaint not found error class.
    """

    def __init__(
            self,
            message: str = "Complaint not found.",
            details: Optional[str] = None
    ):
        super().__init__(
            message, status.HTTP_500_INTERNAL_SERVER_ERROR, details
        )


class APIError(AppException):
    """
    API error class.
    """
    def __init__(
            self,
            message: str = "API error.",
            details: Optional[str] = None
    ):
        super().__init__(
            message, status.HTTP_500_INTERNAL_SERVER_ERROR, details
        )


class TooManyRequests(AppException):
    def __init__(
            self,
            message: str = "Too often requests.",
            details: Optional[str] = None
    ):
        super().__init__(
            message, status.HTTP_429_TOO_MANY_REQUESTS, details
        )


class AIException(AppException):
    def __init__(
            self,
            message: str,
            details: Optional[str] = None
    ):
        super().__init__(
            message, status.HTTP_500_INTERNAL_SERVER_ERROR, details
        )
