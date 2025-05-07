from io import BytesIO
from PIL import Image

from src.application.interfaces import ImageOptimizerService


class ImageOptimizerServiceImpl(ImageOptimizerService):
    @staticmethod
    def optimize_image(
        data: bytes,
        *,
        max_dim_px: int = 1280,
        quality: int = 85,
        format_override: str | None = None,
    ) -> bytes:
        with Image.open(BytesIO(data)) as img:
            fmt = format_override or img.format
            if fmt == "PNG" and img.mode in {"RGB", "L"} and format_override is None:
                fmt = "JPEG"

            if fmt in {"JPEG", "WEBP"} and img.mode in {"RGBA", "P"}:
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1])
                img = bg
            elif fmt in {"JPEG", "WEBP"} and img.mode != "RGB":
                img = img.convert("RGB")

            w, h = img.size
            if max(w, h) > max_dim_px:
                ratio = max_dim_px / max(w, h)
                img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

            out = BytesIO()
            save_opts: dict = dict(optimize=True)
            if fmt in {"JPEG", "WEBP"}:
                save_opts["quality"] = quality
                if fmt == "JPEG":
                    save_opts["progressive"] = True
            img.save(out, format=fmt, **save_opts)
            return out.getvalue()
