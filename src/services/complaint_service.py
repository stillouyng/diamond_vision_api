from typing import (
    Any, Sequence
)

from sqlalchemy import Row, RowMapping

from src.core.config import logger
from src.core.exceptions import (
    DatabaseNotFound, RepositoryError, ServiceError, ComplaintNotFound
)
from src.models.models import Complaint
from src.models.schemas import (
    ComplaintCreate, ComplaintUpdate, ComplaintFilters
)
from src.repositories import ComplaintRepository


class ComplaintService:
    def __init__(self, repository: ComplaintRepository):
        self.repository = repository

    async def add_complaint(
            self,
            complaint_data: ComplaintCreate
    ) -> Complaint:
        """
        Adds a complaint to the database.
        :param complaint_data: Complaint data as a ComplaintCreate schema.
        :raises DatabaseNotFound: Database not found.
        :raises RepositoryError: Raises on SQLAlchemyError | unknown errors.
        :raises ServiceError: Raised on unexpected errors.
        :return: Complaint object.
        """
        try:
            logger.info(
                f"Creates a complaint: {complaint_data.text[:20]}..."
            )
            complaint = await self.repository.create_complaint(
                complaint_data
            )
            logger.info(f"Complaint created successfully. ID: {complaint.id}")
            return complaint
        except DatabaseNotFound as e:
            logger.error(f"Database not found: {e.details}")
            raise
        except RepositoryError as e:
            logger.error(f"Repository error: {e.details}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error creating complaint: {e}",
                exc_info=True
            )
            raise ServiceError("Complaint creation failed", details=str(e))

    async def update_complaint(
            self, complaint_data: ComplaintUpdate
    ) -> Complaint:
        """
        Updates a complaint from the database.
        :param complaint_data: Complaint data as a ComplaintUpdate schema.
        :return: Complaint object.
        """
        try:
            logger.info(
                f"Updates a complaint. ID: {complaint_data.id}"
            )
            complaint = await self.repository.update_complaint(
                complaint_data
            )
            logger.info(f"Complaint updated successfully. ID: {complaint.id}")
            return complaint
        except DatabaseNotFound as e:
            logger.error(f"Database not found: {e.details}")
            raise
        except RepositoryError as e:
            logger.error(f"Repository error: {e.details}")
            raise
        except ComplaintNotFound as e:
            logger.error(f"Complaint not found: {e.details}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error updating complaint: {e}",
                exc_info=True
            )
            raise ServiceError(
                "Complaint update failed",
                details=str(e)
            )

    async def get_complaints_by_time_range(
            self, filters: ComplaintFilters,
    ) -> Sequence[Row[Any] | RowMapping | Any] | None:
        """
        Returns a list of complaints based on the time created.
        :param filters: ComplaintFilters object.
        :raises ServiceError: Raises on unexpected errors.
        :return: List[Complaint] if rows exists, None otherwise.
        """
        try:
            logger.info(
                f"Finds complaints by filters: {filters}"
            )
            complaints = await self.repository.get_complaints_list(
                filters
            )
            return complaints
        except DatabaseNotFound as e:
            logger.error(f"Database not found: {e.details}")
            raise
        except RepositoryError as e:
            logger.error(f"Repository error: {e.details}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error finding complaints: {e}")
            raise ServiceError(
                "Get complaints by time range failed",
                details=str(e)
            )
