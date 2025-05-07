from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException

from src.schemas.users import AccessTokenResponse, LoginUserSchema, RegisterUserSchema
from src.utils.broker_provider import BrokerProvider
from src.utils.jwt_auth import JWTTokenGenerator


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
@inject
async def register_user(
    data: RegisterUserSchema,
    broker_provider: FromDishka[BrokerProvider],
    jwt_generator: FromDishka[JWTTokenGenerator],
) -> AccessTokenResponse:
    """
    Register a new user
    """
    result = await broker_provider.rpc(
        queue="users.register",
        payload=data.model_dump(),
    )

    if "id" not in result:
        raise HTTPException(status_code=400, detail="User registration failed")

    access_token = jwt_generator.generate_for_user(result["id"])
    return AccessTokenResponse(access_token=access_token)



@router.post("/login")
@inject
async def login_user(
    data: LoginUserSchema,
    broker_provider: FromDishka[BrokerProvider],
    jwt_generator: FromDishka[JWTTokenGenerator],
) -> AccessTokenResponse:
    """
    Login user
    """
    result = await broker_provider.rpc(
        queue="users.login",
        payload=data.model_dump(),
    )

    if "id" not in result:
        raise HTTPException(status_code=400, detail="User registration failed")

    access_token = jwt_generator.generate_for_user(result["id"])
    return AccessTokenResponse(access_token=access_token)
