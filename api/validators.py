from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def my_year_validator(value):
    if value < 1 or value > datetime.now().year + 5:
        raise ValidationError(
            _('%(value)s is not a correcrt year!'),
            params={'value': value},
        )


