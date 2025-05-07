from typing import Annotated
from fastapi import Depends
import aiohttp

from src.config import Config, get_config
from src.adapters.aiohttp_gateway_router import AiohttpGatewayRouter, get_session


def get_aiohttp_gateway_router(
    session: Annotated[aiohttp.ClientSession, Depends(get_session)],
    config: Annotated[Config, Depends(get_config)],
) -> AiohttpGatewayRouter:
    return AiohttpGatewayRouter(session, config)
