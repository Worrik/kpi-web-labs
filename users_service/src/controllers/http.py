from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import inject, FromDishka

from src.application.dto import LoginUserDTO, RegisterUserDTO
from src.application.interactors import LoginUserInteractor, RegisterUserInteractor
from src.controllers.schemas import LoginUserSchema, RegisterUserSchema
from src.exceptions.database_exceptions import IntegrityError


api_router = APIRouter()


@api_router.post("/login")
@inject
async def login(
    data: LoginUserSchema,
    interactor: FromDishka[LoginUserInteractor],
) -> dict:
    dto = LoginUserDTO(email=data.email)
    token = await interactor(dto)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token}


@api_router.post("/register")
@inject
async def register(
    data: RegisterUserSchema,
    interactor: FromDishka[RegisterUserInteractor],
) -> dict:
    dto = RegisterUserDTO(name=data.name, email=data.email)
    try:
        token = await interactor(dto)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"access_token": token}
