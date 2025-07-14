from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.enums import (
    ComplaintSentiment, ComplaintCategory
)


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
    """Mocked ComplaintRepository."""
    from src.repositories import ComplaintRepository
    return ComplaintRepository(mock_session)
