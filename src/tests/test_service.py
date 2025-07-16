from datetime import datetime

import pytest

from src.models.schemas import (
    ComplaintCreate, ComplaintUpdate,
    ComplaintFilters
)
from src.models.models import Complaint
from src.core.exceptions import (
    RepositoryError, ServiceError, ComplaintNotFound
)


@pytest.mark.asyncio
async def test_add_complaint_success(service, mock_repo):
    """Valid add a new complaint."""
    test_data = ComplaintCreate(text="Test complaint")

    mock_repo.create_complaint.return_value = Complaint(
        id=1,
        text=test_data.text
    )

    result = await service.add_complaint(test_data)

    assert result.id == 1
    mock_repo.create_complaint.assert_awaited_once_with(test_data)


@pytest.mark.asyncio
async def test_add_complaint_mock_repository_error(service, mock_repo):
    """Error adding a complaint."""
    mock_repo.create_complaint.side_effect = RepositoryError("DB error")

    with pytest.raises(RepositoryError):
        await service.add_complaint(ComplaintCreate(text="Test"))


@pytest.mark.asyncio
async def test_add_complaint_unexpected_error(service, mock_repo):
    """Error adding a complaint."""
    mock_repo.create_complaint.side_effect = Exception("Unexpected")

    with pytest.raises(ServiceError):
        await service.add_complaint(ComplaintCreate(text="Test"))


@pytest.mark.asyncio
async def test_update_complaint_not_found(service, mock_repo):
    """Error database not found"""
    mock_repo.update_complaint.side_effect = ComplaintNotFound("Not found")

    with pytest.raises(ComplaintNotFound):
        await service.update_complaint(ComplaintUpdate(id=1))


@pytest.mark.asyncio
async def test_get_complaints_with_filters(service, mock_repo):
    """Valid get complaints with filters."""
    filters = ComplaintFilters(
        timestamp={
            "start_date": datetime(2025, 7, 13),
            "end_date": datetime(2025, 7, 15)
        }
    )
    mock_repo.get_complaints_list.return_value = [
        Complaint(id=1),
        Complaint(id=2)
    ]

    result = await service.get_complaints_by_time_range(filters)

    assert len(result) == 2
    mock_repo.get_complaints_list.assert_awaited_once_with(filters)
