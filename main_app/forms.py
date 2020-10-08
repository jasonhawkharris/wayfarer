from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class User_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']


class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['hometown', 'photo']


class UpdateProfile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['hometown', 'photo']


class Login_Form(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
