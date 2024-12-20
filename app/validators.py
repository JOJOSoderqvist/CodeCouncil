import re

from django.core.exceptions import ValidationError

def external_password_validator(password):
    if len(password) < 6:
        raise ValidationError('Пароль должен состоять минимум из 6 символов')


def unified_username_validator(username):
    if len(username) < 3 or len(username) > 20:
        raise ValidationError('Имя пользователя должно быть размером от 3-х до 20 символов')


def question_title_validator(question):
    if len(question) < 3:
        raise ValidationError('Вопрос должен состоять минимум из 3-х символов')


def tags_validator(tags):
    comma_tag_pattern = re.compile(r'^(\w+)(,\w+)*$')
    space_tag_pattern = re.compile(r'^(\w+)(\s\w+)*$')
    if len(tags) < 1:
        raise ValidationError('Тег должен содержать минимум 1 символ')
    if not (comma_tag_pattern.match(tags) or space_tag_pattern.match(tags)):
        raise ValidationError('Теги должны быть введены в таком формате: "тег1,тег2,тег3" или "тег1 тег2 тег3"')

    tags_list = tags.split(',') if ',' in tags else tags.split(' ')
    for tag in tags_list:
        if len(tag) > 10:
            raise ValidationError(f'Тэг "{tag}" слишком длинный. Длина не должна превышать 10 символов.')
