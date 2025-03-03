from datetime import timedelta
from typing import AsyncIterable
from dishka import AnyOf, Provider, Scope, from_context, provide
from faststream.broker.core.usecase import BrokerUsecase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.interactors import LoginUserInteractor, RegisterUserInteractor
from src.application.interfaces import DBSession, JWTTokenGenerator, UserRepo
from src.config import Config
from src.infrastructure.database import new_session_maker
from src.infrastructure.jwt_token import JWTTokenGeneratorImpl
from src.infrastructure.repositories import UserRepoImpl


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    broker = from_context(provides=BrokerUsecase, scope=Scope.APP)

    user_repo = provide(UserRepoImpl, scope=Scope.REQUEST, provides=UserRepo)

    login_user_interactor = provide(LoginUserInteractor, scope=Scope.REQUEST)
    register_user_interactor = provide(RegisterUserInteractor, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, DBSession]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_jwt_token_generator(self, config: Config) -> JWTTokenGenerator:
        return JWTTokenGeneratorImpl(
            secret_key=config.jwt.secret_key,
            algorithm=config.jwt.algorithm,
            expiration_delta=timedelta(seconds=config.jwt.expiration_delta),
        )
