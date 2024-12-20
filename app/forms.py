from django import forms

from app.validators import *


class RegisterForm(forms.Form):
    django_username = forms.CharField(max_length=20, validators=[unified_username_validator])
    email = forms.EmailField()
    username = forms.CharField(validators=[unified_username_validator])
    password = forms.CharField(validators=[external_password_validator])
    repeat_password = forms.CharField()
    profile_img = forms.ImageField()

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if not email:
            self.add_error('email', 'Email field must be in right format')
        if not password:
            self.add_error('password', 'Password is too common')
        if password and repeat_password:
            if password != repeat_password:
                self.add_error('repeat_password', 'Passwords must match')

        return cleaned_data


class LoginForm(forms.Form):
    django_username = forms.CharField(max_length=20, validators=[unified_username_validator])
    password = forms.CharField()


class UserEditForm(forms.Form):
    django_username = forms.CharField(max_length=20, required=False, validators=[unified_username_validator])
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False, validators=[unified_username_validator])
    profile_img = forms.ImageField(required=False)

    # def clean(self):
    #     cleaned_data = super(UserEditForm, self).clean()
    #     # email = cleaned_data.get('email')
    #     # if not email:
    #     #     self.add_error('email', 'Email field must be in right format')
    #     return cleaned_data


class NewQuestionForm(forms.Form):
    title = forms.CharField(max_length=20, validators=[question_title_validator])
    text = forms.CharField(max_length=1000)
    tags = forms.CharField(validators=[tags_validator])


class NewAnswerForm(forms.Form):
    answer_text = forms.CharField(max_length=1000)

class EditQuestionForm(forms.Form):
    title = forms.CharField(max_length=20, validators=[question_title_validator])
    text = forms.CharField(max_length=1000)

class EditAnswerForm(forms.Form):
    text = forms.CharField(max_length=1000)
