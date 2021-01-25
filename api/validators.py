import datetime as dt

from django.core.exceptions import ValidationError


def year_validator(value):
    if value < 1900 or value > dt.datetime.now().year:
        raise ValidationError(f'{value} is not a correcrt year!')
