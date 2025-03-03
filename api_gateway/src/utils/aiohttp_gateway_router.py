import logging
from http import HTTPMethod, HTTPStatus
from typing import Any

import aiohttp

from src.exceptions.exceptions import GatewayRouterException, NotFoundException
from src.config import Config


logger = logging.getLogger()


class AiohttpGatewayRouter:
    def __init__(self, session: aiohttp.ClientSession, config: Config):
        self.session = session
        self.config = config

    async def __call__(
        self,
        service_name: str,
        route: str,
        headers: dict[str, Any],
        method: str = HTTPMethod.GET,
        body: bytes | None = None,
    ) -> tuple[bytes, int]:
        service = next((s for s in self.config.services if s.name == service_name), None)
        if service is None:
            raise NotFoundException
        try:
            async with self.session.request(
                method=method,
                url=service.url
                + (route[:-1] if route.endswith("/") else route),
                headers=self._get_headers(headers),
                data=body,
            ) as response:
                response_body = b""
                if response.status != HTTPStatus.NO_CONTENT:
                    response_body = await response.content.read()
            return response_body, response.status
        except Exception as e:
            logger.exception(f"{service.name}: {e}")
            raise GatewayRouterException from e

    @staticmethod
    def _get_headers(headers: dict[str, Any]) -> dict[str, Any]:
        return headers


class AiohttpSessionEngine:
    def __init__(self) -> None:
        self.session: None | aiohttp.ClientSession = None

    async def __call__(self) -> aiohttp.ClientSession:
        if self.session is None:
            connector = aiohttp.TCPConnector(limit_per_host=100)
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self.session


get_session = AiohttpSessionEngine()
