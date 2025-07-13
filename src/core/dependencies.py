from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated, Any, Coroutine

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import api_settings
from src.core.database import AsyncSessionLocal
from src.core.external_api import ExternalAPIClient
from src.repositories import ComplaintRepository
from src.services import ComplaintService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Async session generator with auto reconnect."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_complaint_repository(
        db: AsyncSession = Depends(get_db)
) -> ComplaintRepository:
    """
    Get async complaint repository.
    :param db: Database session.
    :return: Complaint repository.
    """
    repository = ComplaintRepository(db)
    return repository


async def get_complaint_service(
        repository: ComplaintRepository = Depends(get_complaint_repository)
) -> ComplaintService:
    """
    Get async complaint service.
    :param repository: Complaint repository.
    :return: Complaint service.
    """
    service = ComplaintService(repository)
    return service


ComplaintRepositoryDep = Annotated[
    ComplaintRepository, Depends(get_complaint_repository)
]
ComplaintServiceDep = Annotated[
    ComplaintService, Depends(get_complaint_service)
]

async def get_api_layer_client() -> AsyncGenerator[ExternalAPIClient, None]:
    try:
        api_client = ExternalAPIClient(
            base_url=api_settings.SENTIMENT_ANALYSIS_BASE_URL,
            extra_headers={"apikey": api_settings.SENTIMENT_ANALYSIS_API_KEY}
        )
        async with api_client:
            yield api_client
    finally:
        pass


async def get_ip_api_client() -> AsyncGenerator[ExternalAPIClient, None]:
    try:
        api_client = ExternalAPIClient(
            base_url=api_settings.IP_API_BASE_URL
        )
        async with api_client:
            yield api_client
    finally:
        pass


async def get_hugging_face_client() -> AsyncGenerator[ExternalAPIClient, None]:
    try:
        api_client = ExternalAPIClient(
            base_url=api_settings.OPEN_ROUTER_BASE_URL,
            extra_headers={
                "Authorization": f"Bearer {api_settings.OPEN_ROUTER_API_KEY}"
            }
        )
        async with api_client:
            yield api_client
    finally:
        pass


ApiLayerClientDep = Annotated[ExternalAPIClient, Depends(get_api_layer_client)]
ApiIPClientDep = Annotated[ExternalAPIClient, Depends(get_ip_api_client)]
ApiHuggingFaceClientDep = Annotated[
    ExternalAPIClient, Depends(get_hugging_face_client)
]
