from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response

from src.adapters.aiohttp_gateway_router import AiohttpGatewayRouter


router = APIRouter(prefix="/images", tags=["images"])


@router.get("/{path:path}")
@inject
async def get_image(path: str, gateway_router: FromDishka[AiohttpGatewayRouter]) -> Response:
    """
    Get image from static files
    """
    print(path)
    body, status_code = await gateway_router(
        service_name="images_processing_service",
        route=f"/images/{path}",
        headers={},
        method="GET",
    )
    return Response(
        content=body,
        status_code=status_code,
    )
