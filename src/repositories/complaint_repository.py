from sqlalchemy import select
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import (
    DatabaseNotFound, RepositoryError, ComplaintNotFound
)
from src.models.models import Complaint
from src.models.schemas import (
    ComplaintCreate, ComplaintUpdate, ComplaintSentimentCreate,
    ComplaintCategoryCreate
)


class ComplaintRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_complaint(
            self,
            complaint: ComplaintCreate,
            complaint_sentiment: ComplaintSentimentCreate,
            complaint_category: ComplaintCategoryCreate
    ) -> Complaint:
        """
        Creates a complaint.
        :param complaint: ComplaintCreate schema.
        :param complaint_sentiment: ComplaintSentimentCreate schema.
        :param complaint_category: ComplaintCategoryCreate schema.
        :raises DatabaseNotFound: Database not found.
        :raises RepositoryError: Raises on SQLAlchemyError | unknown errors.
        :return: Complaint object.
        """
        try:
            db_complaint = Complaint(
                text=complaint.text,
                sentiment=complaint_sentiment.sentiment,
                category=complaint_category.category
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
