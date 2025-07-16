import pytest
from unittest.mock import AsyncMock

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from src.core.dependencies import ComplaintServiceDep, ApiLayerClientDep, \
    ApiIPClientDep, ApiHuggingFaceClientDep
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


@pytest.fixture
def mock_dependencies():
    """Mocks all external dependencies for the endpoint"""
    return {
        "service": AsyncMock(spec=ComplaintService),
        "api_layer": AsyncMock(spec=ExternalAPIClient),
        "api_ip": AsyncMock(spec=ExternalAPIClient),
        "api_hf": AsyncMock(spec=ExternalAPIClient)
    }


@pytest.fixture
def client(mock_dependencies):
    from src.api import complaints_router
    app = FastAPI()
    app.include_router(complaints_router, prefix="test/api/complaints")

    app.dependency_overrides.update({
        ComplaintServiceDep: lambda: mock_dependencies["service"],
        ApiLayerClientDep: lambda: mock_dependencies["api_layer"],
        ApiIPClientDep: lambda: mock_dependencies["api_ip"],
        ApiHuggingFaceClientDep: lambda: mock_dependencies["api_hf"]
    })

    return TestClient(app)
