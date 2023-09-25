from django import forms
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm 
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    class Meta:
        model = User
        fields = [ 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus':True}))


