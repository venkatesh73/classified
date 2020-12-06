from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='lni-user', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Fullname'}))
    username = forms.EmailField(label='lni-envelope', max_length=255, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder' : 'Email Address'}))
    mobile = forms.CharField(label='lni-mobile', max_length=25, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Mobile'}))
    password1 = forms.CharField(label='lni-lock', min_length=8, max_length=25, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : 'Password'}))
    password2 = forms.CharField(label='lni-lock', max_length=25, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : 'Retype Password'}))
    agree = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))

    class Meta:
        model = User
        fields = ["first_name", "username", "mobile", "password1", "password2", "agree"]

