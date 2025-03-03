from src.application import interfaces
from src.application.dto import LoginUserDTO, RegisterUserDTO


class LoginUserInteractor:
    def __init__(
        self,
        user_repo: interfaces.UserRepo,
        jwt_token_generator: interfaces.JWTTokenGenerator,
    ) -> None:
        self.user_repo = user_repo
        self.jwt_token_generator = jwt_token_generator

    async def __call__(self, dto: LoginUserDTO) -> str | None:
        user = await self.user_repo.get_by_email(dto.email)
        if not user:
            return None
        return self.jwt_token_generator.generate_for_user(user)


class RegisterUserInteractor:
    def __init__(
        self,
        user_repo: interfaces.UserRepo,
        jwt_token_generator: interfaces.JWTTokenGenerator,
    ) -> None:
        self.user_repo = user_repo
        self.jwt_token_generator = jwt_token_generator

    async def __call__(self, dto: RegisterUserDTO) -> str:
        user = await self.user_repo.create(dto.name, dto.email)
        return self.jwt_token_generator.generate_for_user(user)
