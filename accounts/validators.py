from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _



error_messages = {
     "invalid_username": _(
        "Username must only contain letters, numbers and underscores."
    ),
    "underscore_start_end": _(
        "Username can't start or end with an underscore."
    ),
    "digit_start_end": _(
        "Username can't start with a number. "
        "Please choose a different username."
    ),
    "consecutive_underscores": _(
        "Username can't contain consecutive underscore."
    ),
    "invalid_age": _(
        "User must be at least 15 years old."
    ),
}


@deconstructible
class UsernameValidator(RegexValidator):
    regex = "^[a-zA-Z0-9_]+$"
    message = error_messages["invalid_username"]
    code = "invalid_username"

    def __call__(self, value):
        if value.startswith("_") or value.endswith("_"):
            raise ValidationError(
                error_messages["underscore_start_end"],
                code = "underscore_start_end",
            )
        if value[0].isdigit():
            raise ValidationError(
                error_messages["digit_start_end"],
                code = "digit_start_end",
            )
        if "__" in value:
            raise ValidationError(
                error_messages["consecutive_underscores"],
                code="consecutive_underscore",
            )
    
        return super().__call__(value)


@deconstructible
class AgeValidator:
    
    def __call__(self, value):
        today = date.today()
        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )
        
        if age < 15:
            raise ValidationError(
                error_messages["invalid_age"],
                code="invalid_age",
            )
        