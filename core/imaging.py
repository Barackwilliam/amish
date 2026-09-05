"""
Kupunguza ukubwa wa picha zinazopakiwa.

Moh'd atapakia picha za simu za 4MB. Bila hii, ukurasa mmoja unaweza kuwa
na picha za 20MB na site itakuwa nzito. Hii inapunguza upana hadi
IMAGE_MAX_WIDTH na kubana ubora, kabla ya kuhifadhi.
"""

import io
import logging

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.files.base import ContentFile
from django.db.models import ImageField

log = logging.getLogger(__name__)

TRANSPARENT_MODES = ("RGBA", "LA", "P")


def optimize(fieldfile):
    """Inapunguza picha mahali pale pale. Ikishindwa, inaacha ya asili."""
    try:
        from PIL import Image, ImageOps
    except ImportError:
        return

    try:
        fieldfile.file.seek(0)
        image = Image.open(fieldfile.file)
        image = ImageOps.exif_transpose(image)

        keeps_alpha = image.mode in TRANSPARENT_MODES
        fmt = "PNG" if keeps_alpha else "JPEG"
        if not keeps_alpha and image.mode != "RGB":
            image = image.convert("RGB")

        max_width = getattr(settings, "IMAGE_MAX_WIDTH", 1800)
        if image.width > max_width:
            height = round(image.height * max_width / image.width)
            image = image.resize((max_width, height), Image.LANCZOS)

        buffer = io.BytesIO()
        if fmt == "JPEG":
            image.save(
                buffer, "JPEG",
                quality=getattr(settings, "IMAGE_QUALITY", 82),
                optimize=True, progressive=True,
            )
        else:
            image.save(buffer, "PNG", optimize=True)

        name = fieldfile.name.rsplit("/", 1)[-1]
        stem = name.rsplit(".", 1)[0]
        extension = "png" if fmt == "PNG" else "jpg"
        fieldfile.save(f"{stem}.{extension}", ContentFile(buffer.getvalue()), save=False)
    except Exception:  # picha mbovu isizuie kuhifadhi
        log.warning("Imeshindikana kupunguza picha %s", fieldfile.name, exc_info=True)


def optimize_on_save(sender, instance, **kwargs):
    for field in sender._meta.get_fields():
        if not isinstance(field, ImageField):
            continue
        fieldfile = getattr(instance, field.name, None)
        if not fieldfile:
            continue
        if isinstance(getattr(fieldfile, "file", None), UploadedFile):
            optimize(fieldfile)
