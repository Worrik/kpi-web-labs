from typing import Annotated

import aiohttp
from fastapi import Depends

from src.config import Config, get_config
from src.utils.aiohttp_gateway_router import AiohttpGatewayRouter, get_session


def get_gateway_router(
    session: Annotated[aiohttp.ClientSession, Depends(get_session)],
    config: Annotated[Config, Depends(get_config)],
) -> AiohttpGatewayRouter:
    return AiohttpGatewayRouter(session, config)
