from datetime import datetime, timedelta
from typing import Any

from fastapi import (
    APIRouter, Request
)
from starlette import status

from src.core.config import logger
from src.core import (
    ComplaintServiceDep,
    ApiLayerClientDep, ApiIPClientDep
)
from src.core.exceptions import APIError, TooManyRequests
from src.models.enums import ComplaintSentiment
from src.models.schemas import (
    ComplaintResponse, ComplaintCreate, ComplaintSentimentCreate
)

router = APIRouter()


ip_request_cache: dict[str, datetime] = {}


async def get_ip_info(
        ip: str,
        client: ApiIPClientDep
) -> dict[str, Any] | None:
    try:
        response = await client.get(f"/json/{ip}")
    except APIError:
        response = None
    return response


@router.post(
    "/add",
    response_model=ComplaintResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_complaint(
        request: Request,
        complaint: ComplaintCreate,
        service: ComplaintServiceDep,
        api_layer_client: ApiLayerClientDep,
        api_ip_client: ApiIPClientDep
):
    """
    Save a new complaint.
    """
    body = complaint.text.encode("utf-8")
    try:

        client_ip = request.client.host
        now = datetime.now()
        last_request: datetime | None = ip_request_cache.get(client_ip, None)

        if last_request and now - last_request < timedelta(seconds=10):
            raise TooManyRequests(
                details=f"Try again "
                        f"In {
                            max(0, round((now - last_request).total_seconds()))
                        } "
                        f"seconds later."
            )
        ip_request_cache[client_ip] = now

        full_ip_info = await get_ip_info(client_ip, api_ip_client)

        logger.info(f"Got user info for {client_ip}: {full_ip_info}")

        sentiment_raw = await api_layer_client.post(
            "sentiment/analysis",
            data=body
        )
        sentiment = ComplaintSentiment(sentiment_raw["sentiment"])
    except APIError:
        sentiment = ComplaintSentiment("unknown")

    complaint_sentiment = ComplaintSentimentCreate(sentiment=sentiment)

    return await service.add_complaint(complaint, complaint_sentiment)
