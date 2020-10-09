from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


""" class User_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2'] """


class Register_Form(UserCreationForm):
    first_name = forms.CharField(max_length=100,)
    last_name = forms.CharField(max_length=100,)
    hometown = forms.CharField(max_length=50)
    photo = forms.CharField(max_length=250)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2', 'hometown', 'photo']



class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['hometown', 'photo']

class UpdateUser_Form(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email']

class UpdateProfile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['hometown', 'photo']


class Login_Form(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
