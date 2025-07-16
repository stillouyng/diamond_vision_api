import asyncio
from typing import (
    Mapping, Any, Optional
)

import httpx

from src.core.config import logger
from src.core.exceptions import APIError


class ExternalAPIClient:
    def __init__(
            self,
            base_url: str,
            extra_headers: Optional[Mapping[str, Any]] = None
    ) -> None:
        self.retries: int = 2
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.__setup_headers(extra_headers),
            timeout=httpx.Timeout(10),
        )

    async def __aenter__(self) -> "ExternalAPIClient":
        return self

    async def __aexit__(self, *exc_info) -> None:
        await self.client.aclose()

    @staticmethod
    def __setup_headers(
            extra_headers: Optional[Mapping[str, Any]] = None
    ) -> Mapping[str, Any]:
        """
        Setup HTTP headers.
        :param extra_headers: Extra HTTP headers. (Authorization, etc.)
        :return: New HTTP headers
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if extra_headers:
            headers.update(extra_headers)
        return headers

    async def __request(
            self,
            method: str,
            url: str,
            **kwargs
    ) -> dict[str, Any]:
        """
        Sends a request to the external API.
        :param method: Method of the request.
        :param endpoint: Full URL of the external API.
        :param kwargs: Additional arguments to pass to the request.
        :raises: APIError when the request fails max attempts.
        :return: HTTP response if successful or None otherwise.
        """

        last_error = None
        async with self.client:
            for attempt in range(0, self.retries):
                try:
                    response = await self.client.request(
                        method=method,
                        url=url,
                        **kwargs
                    )
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPStatusError as e:
                    last_error = APIError("HTTP Status Error", str(e))
                    logger.warning(
                        f"Attempt {attempt + 1}/{self.retries + 1} failed. "
                        f"API returned status code {e.response.status_code}. "
                    )
                except httpx.HTTPError as e:
                    last_error = APIError("HTTP Status Error", str(e))
                    logger.warning(
                        f"Attempt {attempt + 1}/{self.retries + 1} failed. "
                        f"{e}"
                    )
                except httpx.TimeoutException as e:
                    last_error = APIError("HTTP Timeout Error", str(e))
                    logger.warning(
                        f"Attempt {attempt + 1}/{self.retries + 1} failed. "
                        f"Timeout error: {e}"
                    )
                except Exception as e:
                    last_error = APIError("Unknown Error", str(e))
                    logger.warning(
                        f"Attempt {attempt + 1}/{self.retries + 1} failed. "
                        f"API returned exception {e}"
                    )

                if attempt < self.retries:
                    await asyncio.sleep(1)

            raise last_error if last_error else APIError(
                "Unknown Error Occurred."
            )

    get = lambda self, e, **kw: self.__request("GET", e, **kw)  # noqa: E731
    post = lambda self, e, **kw: self.__request("POST", e, **kw)  # noqa: E731
    put = lambda self, e, **kw: self.__request("PUT", e, **kw)  # noqa: E731
    delete = lambda self, e, **kw: self.__request(  # noqa: E731
        "DELETE", e, **kw
    )
