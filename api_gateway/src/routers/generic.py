from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response

import http

from src.dependencies.gateway_router import get_gateway_router
from src.utils.aiohttp_gateway_router import AiohttpGatewayRouter


router = APIRouter()


ALL_METHODS = [method.value for method in http.HTTPMethod]


@router.api_route("/{service}/{path:path}", methods=ALL_METHODS)
async def generic_handler(
    service: str,
    path: str,
    request: Request,
    response: Response,
    redirect: Annotated[AiohttpGatewayRouter, Depends(get_gateway_router)],
) -> bytes:
    full_path = f"/{path}?{request.url.query}" if request.url.query else f"/{path}"
    body, response.status_code = await redirect(
        service, full_path, dict(request.headers), request.method, await request.body()
    )
    return body
