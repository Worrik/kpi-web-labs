from io import BytesIO
from pathlib import Path
from typing import Final
from PIL import Image
from uuid import uuid4

from src.application.interfaces import ImageSaverService
from src.config import Config


class ImageSaverServiceImpl(ImageSaverService):
    def __init__(self, config: Config) -> None:
        self._dir: Final[Path] = Path(config.static_files.static_dir)
        self._route: Final[str] = config.static_files.static_route.rstrip("/")

    def save_image(self, data: bytes, dst: str | None = None, filename: str | None = None) -> str:
        with Image.open(BytesIO(data)) as img:
            fmt = img.format

        if not fmt:
            raise ValueError("Image format not detected")

        ext = "jpg" if fmt == "jpeg" else fmt

        target_dir = self._dir / dst if dst else self._dir
        target_dir.mkdir(parents=True, exist_ok=True)

        if filename:
            filename = f"{filename}.{ext}"
        else:
            filename = f"{uuid4().hex}.{ext}"

        path = target_dir / filename
        path.write_bytes(data)

        url_parts = [self._route]
        if dst:
            url_parts.append(dst.strip("/"))
        url_parts.append(filename)
        return "/".join(url_parts)
