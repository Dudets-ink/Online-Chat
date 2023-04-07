from django import forms
from django.contrib.auth.forms import UserCreationForm  
from .models import User 
  


class SignUpForm(UserCreationForm):  
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, required=True)
    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')
    
    
class SignInForm(forms.Form):
    username_email = forms.CharField(max_length=50, required=True)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, required=True)