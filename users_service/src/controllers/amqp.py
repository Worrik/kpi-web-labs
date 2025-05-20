from dishka import FromDishka
from faststream.rabbit import RabbitRouter
from uuid import UUID

from src.application.dto import LoginUserDTO, RegisterUserDTO, GetUsersByIdsDTO
from src.application.interactors import LoginUserInteractor, RegisterUserInteractor, GetUsersByIdsInteractor
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


@amqp_router.subscriber("users.get_by_ids")
async def get_users_by_ids(
    user_ids: list[UUID],
    interactor: FromDishka[GetUsersByIdsInteractor],
) -> list[UserSchema]:
    dto = GetUsersByIdsDTO(user_ids=user_ids)
    users = await interactor(dto)
    return [
        UserSchema(
            id=user.id,
            created_at=user.created_at,
            name=user.name,
            email=user.email,
        )
        for user in users
    ]
