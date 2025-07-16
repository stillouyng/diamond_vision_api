from datetime import datetime
from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from src.core.exceptions import DatabaseNotFound, RepositoryError
from src.models.models import Complaint
from src.models.schemas import ComplaintCreate, ComplaintFilters


@pytest.mark.asyncio
async def test_create_complaint_success(
        repo, mock_session, valid_complaint_data
):
    """Successful complaint creation."""
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    result = await repo.create_complaint(
        ComplaintCreate(
            **valid_complaint_data
        )
    )

    assert isinstance(result, Complaint)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_complaint_database_error(repo, mock_session):
    """Database error."""
    mock_session.add.side_effect = OperationalError(
        "DB error", {}, None
    )

    with pytest.raises(DatabaseNotFound):
        await repo.create_complaint(ComplaintCreate(text="Test"))


@pytest.mark.asyncio
async def test_get_complaints_list_success(repo, mock_session):
    """Valid mocked get_complaints_list."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Complaint(id=1),
        Complaint(id=2)
    ]

    mock_session.execute.return_value = mock_result

    filters = ComplaintFilters()
    result = await repo.get_complaints_list(filters)

    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_complaints_list_with_filters(repo, mock_session):
    """Update with filters."""
    mock_complaints = [Complaint(id=1), Complaint(id=2)]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = mock_complaints

    mock_session.execute.return_value = mock_result

    filters = ComplaintFilters(
        timestamp={"start_date": datetime(2025, 7, 13),
                   "end_date": datetime(2025, 7, 15)}
    )
    result = await repo.get_complaints_list(filters)

    assert len(result) == 2
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_complaints_list_empty(repo, mock_session):
    """ComplaintsList response is empty."""

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = None

    mock_session.execute.return_value = mock_result

    result = await repo.get_complaints_list(ComplaintFilters())
    assert result is None


@pytest.mark.asyncio
async def test_repository_error_handling(repo, mock_session):
    mock_session.execute.side_effect = SQLAlchemyError("DB fail")

    with pytest.raises(RepositoryError):
        await repo.get_complaints_list(ComplaintFilters())
