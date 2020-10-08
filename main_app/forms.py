from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile


class Login_Form(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
