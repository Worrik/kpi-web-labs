import base64

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
        img_data = dto.data.encode()
        content = base64.b64decode(img_data)
        optimized_image = self.image_optimizer.optimize_image(content)
        return self.image_saver.save_image(optimized_image)
