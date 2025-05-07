from datetime import timedelta
from typing import AsyncIterable
from dishka import Provider, Scope, from_context, provide
from faststream.rabbit import RabbitBroker

from src.config import Config
from src.utils.broker_provider import BrokerProvider
from src.utils.jwt_auth import JWTTokenGenerator, JWTTokenValidator


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_broker(self, config: Config) -> AsyncIterable[RabbitBroker]:
        async with RabbitBroker(url=config.rabbitmq.url) as broker:
            yield broker

    @provide(scope=Scope.REQUEST)
    async def get_broker_provider(self, broker: RabbitBroker) -> BrokerProvider:
        return BrokerProvider(broker)

    @provide(scope=Scope.APP)
    def get_jwt_token_generator(self, config: Config) -> JWTTokenGenerator:
        return JWTTokenGenerator(
            secret_key=config.jwt.secret_key,
            algorithm=config.jwt.algorithm,
            expiration_delta=timedelta(minutes=config.jwt.access_token_expire_minutes),
        )

    @provide(scope=Scope.APP)
    def get_jwt_token_validator(self, config: Config) -> JWTTokenValidator:
        return JWTTokenValidator(
            secret_key=config.jwt.secret_key,
            algorithm=config.jwt.algorithm,
        )
