import re

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not re.findall("^380[0-9]{2}-[0-9]{3}-[0-9]{2}-[0-9]{2}$"):
        raise ValidationError("Please enter the correct phone number format")

    return value
