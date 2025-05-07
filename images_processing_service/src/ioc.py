from dishka import Provider, Scope, from_context, provide
from faststream.broker.core.usecase import BrokerUsecase
from src.application.interactors import OptimizeImageInteractor
from src.application.interfaces import ImageOptimizerService, ImageSaverService

from src.config import Config
from src.infrastructure.services.image_optimizer import ImageOptimizerServiceImpl
from src.infrastructure.services.image_saver import ImageSaverServiceImpl


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    broker = from_context(provides=BrokerUsecase, scope=Scope.APP)

    image_optimizer = provide(ImageOptimizerServiceImpl, scope=Scope.REQUEST, provides=ImageOptimizerService)
    image_saver = provide(ImageSaverServiceImpl, scope=Scope.REQUEST, provides=ImageSaverService)

    optimize_image_interactor = provide(OptimizeImageInteractor, scope=Scope.REQUEST)
