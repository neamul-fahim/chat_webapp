# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    # You can add additional fields or customization if needed
    class Meta:
        model = AuthenticationForm
        fields = ['username', 'password']
