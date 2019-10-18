# -*- coding: utf-8 -*-

from  django.contrib.auth.password_validation import MinimumLengthValidator

from django.utils.translation import ugettext as _, ungettext
from django.core.exceptions import ValidationError

class CustomLengthValidator(MinimumLengthValidator):
    """
    Validate whether the password is of a minimum length.
    """
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ungettext(                    
                    "This password is too short. It must contain at least %(min_length)d character.",
					u"Этот пароль слишком короткий. Необходимо минимум %(min_length)d символов.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ungettext(
            "Your password must contain at least %(min_length)d character.",
            "Your password must contain at least %(min_length)d characters.",
            self.min_length
        ) % {'min_length': self.min_length}
		
		
		
class CustomNumericValidator(object):
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _(u"Пароль не должен полностью состоять из цифр"),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Your password can't be entirely numeric.")