from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class AuthForm(forms.Form):
    template_name = 'users/form_snippet.html'
    
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    template_name = 'users/form_snippet.html'

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')
