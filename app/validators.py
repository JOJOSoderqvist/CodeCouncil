import re

from django.core.exceptions import ValidationError


def external_password_validator(password):
    if len(password) < 6:
        raise ValidationError('Password must be at least 6 characters')


def unified_username_validator(username):
    if len(username) < 3 or len(username) > 20:
        raise ValidationError('Username must be between 3 and 20 characters')


def question_title_validator(question):
    if len(question) < 3:
        raise ValidationError('Question must be between at least 3 characters')


def tags_validator(tags):
    comma_tag_pattern = re.compile(r'^(\w+)(,\w+)*$')
    space_tag_pattern = re.compile(r'^(\w+)(\s\w+)*$')
    if len(tags) < 1:
        raise ValidationError('Tags must be at least 1 character')
    if not (comma_tag_pattern.match(tags) or space_tag_pattern.match(tags)):
        raise ValidationError('Tags must be in the format of "tag1,tag2,tag3" or "tag1 tag2 tag3"')
