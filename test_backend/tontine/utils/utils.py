import secrets

from django.core.exceptions import ValidationError

LENGTH = 20


def generate_tontine_name():
    return secrets.token_hex(LENGTH)


def validate_frequency_duration(value):
    if value > 0:
        return value
    else:
        raise ValidationError("This field accepts positive integers only")
