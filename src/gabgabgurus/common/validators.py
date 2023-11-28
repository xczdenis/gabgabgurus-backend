from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from PIL import Image


@deconstructible
class MaxFileWeightValidator(MaxValueValidator):
    def clean(self, x):
        return x.size

    def compare(self, a, b):
        is_error = super().compare(a, b)
        if is_error:
            max_size = round(b / 1024)
            current_size = round(a / 1024)
            self.message = _(f"File size must be no more then {max_size} Kb. Current size: {current_size} Kb")

        return is_error


@deconstructible
class MaxImageSizeValidator:
    message = _("Image size must be no more then %(limit_size)s. Current size: %(current_size)s.")
    code = "invalid_image_size"

    def __init__(self, limit_width: int, limit_height: int, message=None, code=None):
        self.limit_width = limit_width
        self.limit_height = limit_height
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        image = value
        if not hasattr(value, "width"):
            image = Image.open(value)
        img_width = image.width
        img_height = image.height
        if img_width > self.limit_width or img_height > self.limit_height:
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    "limit_size": f"{self.limit_width}x{self.limit_height}",
                    "current_size": f"{img_width}x{img_height}",
                },
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.limit_height == other.limit_height
            and self.limit_width == other.limit_width
            and self.message == other.message
            and self.code == other.code
        )
