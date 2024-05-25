from django.core.exceptions import ValidationError


def external_password_validator(password):
    if len(password) < 6:
        raise ValidationError('Password must be at least 6 characters')
    if not password.isnumeric():
        raise ValidationError('Password must contain only numbers and characters')


def unified_username_validator(username):
    if len(username) < 3 or len(username) > 20:
        raise ValidationError('Username must be between 3 and 20 characters')