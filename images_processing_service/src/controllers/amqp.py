from dishka import FromDishka
from faststream.rabbit import RabbitRouter
from src.application.dto import OptimizeImageDTO
from src.application.interactors import OptimizeImageInteractor

from src.controllers.schemas import OptimizeImageSchema


amqp_router = RabbitRouter()


@amqp_router.subscriber("image_processing.optimize_image")
async def optimize_image(
    data: OptimizeImageSchema,
    interactor: FromDishka[OptimizeImageInteractor],
) -> str:
    dto = OptimizeImageDTO(data=data.data)
    return interactor(dto)
