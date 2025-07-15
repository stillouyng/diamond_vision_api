import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.external_api import ExternalAPIClient
from src.models.enums import (
    ComplaintSentiment, ComplaintCategory
)

from src.repositories import ComplaintRepository
from src.services import ComplaintService


@pytest.fixture
def valid_complaint_data():
    """Create valid complaint data."""
    return {
        "text": "What's wrong with the pay button?",
        "sentiment": ComplaintSentiment.POSITIVE,
        "category": ComplaintCategory.TECHNICAL
    }


@pytest.fixture
def mock_session():
    """AsyncSession mock fixture."""
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture
def repo(mock_session):
    """ComplaintRepository with mocked session."""
    return ComplaintRepository(mock_session)


@pytest.fixture
def mock_repo(mock_session):
    """Mocked ComplaintRepository."""
    return AsyncMock()


@pytest.fixture
def service(mock_repo):
    """ComplaintService with mocked session."""
    return ComplaintService(mock_repo)


@pytest.fixture
def mock_client():
    """Mocked ExternalAPI client."""
    return ExternalAPIClient(base_url="http://test.com")
