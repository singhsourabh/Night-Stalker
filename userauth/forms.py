from django import forms
from .models import *
from django.contrib.auth.models import User

class userReg(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'uname', 'placeholder':'Enter the username'}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'mail', 'placeholder':'Enter the email'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'pass'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'cpass'}), required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']