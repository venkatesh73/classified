from django import forms

class SignInForm(forms.Form):
    username = forms.CharField(label='lni-envelope', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Email Address'}))
    password = forms.CharField(label='lni-lock', max_length=25, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : 'Password'}))
    keep_loggedin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))