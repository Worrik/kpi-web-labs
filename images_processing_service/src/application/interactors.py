from src.application import interfaces
from src.application.dto import OptimizeImageDTO


class OptimizeImageInteractor:
    def __init__(
        self,
        image_optimizer: interfaces.ImageOptimizerService,
        image_saver: interfaces.ImageSaverService,
    ) -> None:
        self.image_optimizer = image_optimizer
        self.image_saver = image_saver

    def __call__(self, dto: OptimizeImageDTO) -> str:
        optimized_image = self.image_optimizer.optimize_image(dto.data)
        return self.image_saver.save_image(optimized_image)
