from django.core.exceptions import ValidationError

IMAGE_EXTENSIONS = ["gif", "jpg", "jpeg", "png", "webp"]
VIDEO_EXTENSIONS = ["webm", "ts", "wmv", "rmvb", "amv", "mp4", "mpg", "mpeg"]


def validate_format(value):
    ext = value.name.split(".")[-1].lower()

    if ext not in IMAGE_EXTENSIONS and ext not in VIDEO_EXTENSIONS:
        raise ValidationError(
            ("%(value)s is not a valid format"),
            params={"ext": ext},
        )


def check_format(value):
    ext = value.split(".")[-1].lower()
    if ext in IMAGE_EXTENSIONS:
        return "image"
    elif ext in VIDEO_EXTENSIONS:
        return "video"
    else:
        raise ValidationError(
            ("%(value)s is not a valid format"),
            params={"ext": ext},
        )
