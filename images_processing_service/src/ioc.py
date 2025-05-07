from dishka import Provider, Scope, from_context
from faststream.broker.core.usecase import BrokerUsecase

from src.config import Config


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    broker = from_context(provides=BrokerUsecase, scope=Scope.APP)
