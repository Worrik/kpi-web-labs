from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Response

from src.adapters.aiohttp_gateway_router import AiohttpGatewayRouter


router = APIRouter(prefix="/images", tags=["images"])


# static files redirect
@router.get("/{path:path}")
async def get_image(path: str, gateway_router: FromDishka[AiohttpGatewayRouter]) -> Response:
    """
    Get image from static files
    """
    body, status_code = await gateway_router(
        service_name="static_files",
        route=f"/images/{path}",
        headers={},
        method="GET",
    )
    return Response(
        content=body,
        status_code=status_code,
    )
