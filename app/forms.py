from django import forms


class RegisterForm(forms.Form):
    django_username = forms.CharField(max_length=20)
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()
    repeat_password = forms.CharField()
