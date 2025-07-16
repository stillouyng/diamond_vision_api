import pytest

from src.core.config import api_settings
from src.core.dependencies import (
    get_hugging_face_client, get_ip_api_client, get_api_layer_client
)
from src.core.external_api import ExternalAPIClient
from src.core.exceptions import APIError


@pytest.mark.asyncio
async def test_client_success(httpx_mock):
    """Successful response."""
    httpx_mock.add_response(
        url="http://test.com/endpoint",
        json={"key": "value"},
        status_code=200
    )

    client = ExternalAPIClient(base_url="http://test.com")
    response = await client.get("/endpoint")

    assert response == {"key": "value"}


@pytest.mark.asyncio
async def test_client_retries(httpx_mock):
    """Client retries."""
    httpx_mock.add_response(
        url="http://test.com/endpoint",
        status_code=500
    )
    httpx_mock.add_response(
        url="http://test.com/endpoint",
        json={"success": True},
        status_code=200
    )

    client = ExternalAPIClient(base_url="http://test.com")
    response = await client.get("/endpoint")

    assert response == {"success": True}
    assert len(httpx_mock.get_requests()) == 2


@pytest.mark.asyncio
async def test_client_failure(httpx_mock):
    """Test client failure."""
    httpx_mock.add_response(
        url="http://test.com/endpoint",
        status_code=500
    )
    httpx_mock.add_response(
        url="http://test.com/endpoint",
        status_code=502
    )

    client = ExternalAPIClient(base_url="http://test.com")
    with pytest.raises(APIError) as exc_info:
        await client.get("/endpoint")

    assert isinstance(exc_info.value, APIError)


@pytest.mark.asyncio
async def test_huggingface_dependency(httpx_mock):
    """Test HuggingFace client dependency with proper async handling"""
    httpx_mock.add_response(
        url=f"{api_settings.OPEN_ROUTER_BASE_URL}endpoint",
        headers={
            "Authorization": f"Bearer {api_settings.OPEN_ROUTER_API_KEY}"
        },
        json={"result": "ok"}
    )

    client_gen = get_hugging_face_client()

    try:
        client = await client_gen.__anext__()
        response = await client.get("/endpoint")
        assert response == {"result": "ok"}

        request = httpx_mock.get_requests()[0]
        assert request.headers[
                   "Authorization"
               ] == f"Bearer {api_settings.OPEN_ROUTER_API_KEY}"
    finally:
        with pytest.raises(StopAsyncIteration):
            await client_gen.__anext__()


@pytest.mark.asyncio
async def test_ip_api_dependency(httpx_mock):
    """Test Api IP client dependency with proper async handling"""
    httpx_mock.add_response(
        url=f"{api_settings.IP_API_BASE_URL}endpoint",
        json={"result": "ok"}
    )

    client_gen = get_ip_api_client()

    try:
        client = await client_gen.__anext__()
        response = await client.get("/endpoint")
        assert response == {"result": "ok"}

        request = httpx_mock.get_requests()[0]
        print(request.url)
        assert request.url == "https://ip-api.com/endpoint"
    finally:
        with pytest.raises(StopAsyncIteration):
            await client_gen.__anext__()


@pytest.mark.asyncio
async def test_api_layer_dependency(httpx_mock):
    """Test ApiLayer client dependency with proper async handling"""
    httpx_mock.add_response(
        url=f"{api_settings.SENTIMENT_ANALYSIS_BASE_URL}endpoint",
        headers={
            "apikey": api_settings.SENTIMENT_ANALYSIS_API_KEY
        },
        json={"result": "ok"}
    )

    client_gen = get_api_layer_client()

    try:
        client = await client_gen.__anext__()
        response = await client.get("/endpoint")
        assert response == {"result": "ok"}

        request = httpx_mock.get_requests()[0]
        assert request.headers[
                   "apikey"
               ] == api_settings.SENTIMENT_ANALYSIS_API_KEY
    finally:
        with pytest.raises(StopAsyncIteration):
            await client_gen.__anext__()
