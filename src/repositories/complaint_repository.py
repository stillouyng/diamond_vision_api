from typing import List, Any, Coroutine, Sequence

from sqlalchemy import select, Row, RowMapping, and_
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import (
    DatabaseNotFound, RepositoryError, ComplaintNotFound
)
from src.models.models import Complaint
from src.models.schemas import (
    ComplaintCreate, ComplaintUpdate, ComplaintFilters
)


class ComplaintRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_complaint(
            self,
            complaint: ComplaintCreate
    ) -> Complaint:
        """
        Creates a complaint.
        :param complaint: ComplaintCreate schema.
        :raises DatabaseNotFound: Database not found.
        :raises RepositoryError: Raises on SQLAlchemyError | unknown errors.
        :return: Complaint object.
        """
        try:
            db_complaint = Complaint(
                text=complaint.text,
                sentiment=complaint.sentiment,
                category=complaint.category,
            )
            self.session.add(db_complaint)
            await self.session.commit()
            await self.session.refresh(db_complaint)
            return db_complaint
        except OperationalError as e:
            raise DatabaseNotFound(details=str(e))
        except SQLAlchemyError as e:
            raise RepositoryError(
                f"Database operation failed",
                details=str(e)
            )
        except Exception as e:
            raise RepositoryError(f"Unexpected error", details=str(e))

    async def update_complaint(
            self,
            complaint_id: int,
            complaint_data: ComplaintUpdate
    ) -> Complaint:
        """
        Updates a complaint.
        :param complaint_id: Complaint ID.
        :param complaint_data: Complaint data as a ComplaintUpdate schema.
        :raises DatabaseNotFound: Database not found.
        :raises RepositoryError: Raises on SQLAlchemyError | unknown errors.
        :raises ComplaintNotFound: Complaint not found.
        :return: Complaint object.
        """
        try:
            result = await self.session.execute(
                select(Complaint)
                .where(Complaint.id == complaint_id)
            )

            complaint = result.scalar_one_or_none()

            if not complaint:
                raise ComplaintNotFound(
                    details=f"Complaint {complaint_id} not found"
                )

            for key, value in complaint_data.dict(exclude_unset=True).items():
                setattr(complaint, key, value)

            await self.session.commit()
            await self.session.refresh(complaint)
            return complaint
        except OperationalError as e:
            raise DatabaseNotFound(details=str(e))
        except SQLAlchemyError as e:
            raise RepositoryError(
                f"Database operation failed",
                details=str(e)
            )
        except Exception as e:
            raise RepositoryError(f"Unexpected error", details=str(e))

    async def get_complaints_list(
            self,
            filters: ComplaintFilters
    ) -> Sequence[Row[Any] | RowMapping | Any] | None:
        """
        Gets a list of complaints by filters.
        :param filters: ComplaintFilters schema.
        :raises DatabaseNotFound: Database not found.
        :raises RepositoryError: Raises on SQLAlchemyError | unknown errors.
        :raises ComplaintNotFound: Complaint not found.
        :return: List of complaints if exists, None otherwise.
        """
        try:
            conditions = []

            if filters.category:
                conditions.append(Complaint.category == filters.category)
            if filters.status:
                conditions.append(Complaint.status == filters.status)
            if filters.sentiment:
                conditions.append(Complaint.sentiment == filters.sentiment)
            if filters.timestamp:
                conditions.append(
                    Complaint.timestamp.between(
                        filters.timestamp['start_date'],
                        filters.timestamp['end_date']
                    )
                )
            query = select(Complaint)
            if conditions: query = query.where(and_(*conditions))
            result = await self.session.execute(query)
            complaints = result.scalars().all()
            return complaints if complaints else None
        except OperationalError as e:
            raise DatabaseNotFound(details=str(e))
        except SQLAlchemyError as e:
            raise RepositoryError(
                f"Database operation failed",
                details=str(e)
            )
        except Exception as e:
            raise RepositoryError(f"Unexpected error", details=str(e))
