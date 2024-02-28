import re

from django.core.exceptions import ValidationError


def calary_validator(value):
    if not re.findall("[0-9]{1,5}|[0-9]{1,5}-[0-9]{1,5}", value):
        raise ValidationError("incorrect format of calary", 400)

    return value
