from dishka.integrations.fastapi import FromDishka, inject
from fastapi import HTTPException, Header

from src.utils.jwt_auth import JWTTokenValidator


@inject
def get_user_id(
    jwt_token_validator: FromDishka[JWTTokenValidator],
    Authorization: str = Header(),
) -> str:
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = Authorization.split(" ")[1]

    try:
        payload = jwt_token_validator.validate(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return user_id
