from abc import abstractmethod
from typing import Protocol


class ImageSaverService(Protocol):
    @abstractmethod
    def save_image(
        self,
        data: bytes,
        dst: str | None = None,
        filename: str | None = None,
    ) -> str: ...


class ImageOptimizerService(Protocol):
    @abstractmethod
    def optimize_image(self, data: bytes) -> bytes: ...
