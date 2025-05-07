from src.application import interfaces
from src.application.dto import LoginUserDTO, RegisterUserDTO
from src.domain.entities import UserDM


class LoginUserInteractor:
    def __init__(self, user_repo: interfaces.UserRepo) -> None:
        self.user_repo = user_repo

    async def __call__(self, dto: LoginUserDTO) -> UserDM | None:
        return await self.user_repo.get_by_email(dto.email)


class RegisterUserInteractor:
    def __init__(self, user_repo: interfaces.UserRepo) -> None:
        self.user_repo = user_repo

    async def __call__(self, dto: RegisterUserDTO) -> UserDM:
        return await self.user_repo.create(
            name=dto.name,
            email=dto.email,
        )
