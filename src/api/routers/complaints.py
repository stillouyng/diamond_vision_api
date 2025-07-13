from datetime import datetime, timedelta
from typing import Any

from fastapi import (
    APIRouter, Request
)
from starlette import status

from src.core.config import logger
from src.core import (
    ComplaintServiceDep,
    ApiLayerClientDep, ApiIPClientDep, ApiHuggingFaceClientDep
)
from src.core.exceptions import APIError, TooManyRequests
from src.models.enums import ComplaintSentiment, ComplaintCategory
from src.models.schemas import (
    ComplaintResponse, ComplaintCreate, ComplaintSentimentCreate,
    ComplaintCategoryCreate
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


async def get_complaint_category(
        text: str,
        client: ApiHuggingFaceClientDep
) -> ComplaintCategory | None:
    """
    Request to OpenRouter (Mistral-7B-v0.3) to classify the complaint category.
    :param text: Input complaint text.
    :param client: External API Client.
    :return: Complaint category if successful, None otherwise.
    """
    try:
        try:
            response = await client.post(
                "api/v1/completions",
                json={
                    "prompt": "Classify the category of complaint "
                              "(technical/payment/neutral): "
                              f"{text}."
                              f"Answer me with one word."
                }
            )
            category_raw = response["choices"][0]["text"]
            category = ComplaintCategory(
                category_raw.split("\n")[0].strip().lower()
            )
            return category
        except APIError:
            return None
        except ValueError:
            if "payment" in category_raw:
                return ComplaintCategory("payment")
            elif "technical" in category_raw:
                return ComplaintCategory("technical")
            elif "neutral" in category_raw:
                return ComplaintCategory("neutral")
            else: return None
    except Exception as e:
        return None


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
        api_ip_client: ApiIPClientDep,
        api_hugging_face_client: ApiHuggingFaceClientDep
):
    """
    Save a new complaint.
    """

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

    classified_category = await get_complaint_category(
        complaint.text,
        api_hugging_face_client
    )
    logger.info(f"Classify complaint response: {classified_category}")

    try:
        body = complaint.text.encode("utf-8")
        sentiment_raw = await api_layer_client.post(
            "sentiment/analysis",
            data=body
        )
        sentiment = ComplaintSentiment(sentiment_raw["sentiment"])
    except APIError:
        sentiment = ComplaintSentiment("unknown")

    complaint_sentiment = ComplaintSentimentCreate(sentiment=sentiment)
    complaint_category = ComplaintCategoryCreate(
        category=classified_category if classified_category else "other"
    )

    return await service.add_complaint(
        complaint,
        complaint_sentiment,
        complaint_category
    )
