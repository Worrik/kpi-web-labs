from dishka import FromDishka
from faststream.rabbit import RabbitRouter

from src.application.dto import LoginUserDTO, RegisterUserDTO
from src.application.interactors import LoginUserInteractor, RegisterUserInteractor
from src.controllers.schemas import (
    ErrorResponse,
    LoginUserSchema,
    RegisterUserSchema,
    UserSchema,
)
from src.exceptions.database_exceptions import IntegrityError


amqp_router = RabbitRouter()


@amqp_router.subscriber("users.register")
async def register_user(
    data: RegisterUserSchema,
    interactor: FromDishka[RegisterUserInteractor],
) -> UserSchema | ErrorResponse:
    dto = RegisterUserDTO(
        name=data.name,
        email=data.email,
    )
    try:
        token = await interactor(dto)
    except IntegrityError:
        return ErrorResponse(detail="User already exists")
    return UserSchema(
        id=token.id,
        created_at=token.created_at,
        name=token.name,
        email=token.email,
    )


@amqp_router.subscriber("users.login")
async def login_user(
    data: LoginUserSchema,
    interactor: FromDishka[LoginUserInteractor],
) -> UserSchema | ErrorResponse:
    dto = LoginUserDTO(email=data.email)
    token = await interactor(dto)
    if not token:
        return ErrorResponse(detail="Invalid credentials")
    return UserSchema(
        id=token.id,
        created_at=token.created_at,
        name=token.name,
        email=token.email,
    )
