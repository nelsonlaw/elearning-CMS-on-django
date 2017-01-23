from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="AB ID", max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class RegisterForm(forms.Form):
    employee_name = forms.CharField(label="Display Name:", max_length=127)
    username = forms.CharField(label="AB ID(for login):", max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    password_again = forms.CharField(label="Password again", max_length=30,
                                     widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
