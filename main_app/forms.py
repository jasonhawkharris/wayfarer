from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, ValidationError
from django.contrib.auth.models import User
from .models import Post, Profile, City


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
                  'email', 'password1', 'password2', 'hometown']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise ValidationError(
                'This email is already registered for this site')
        return email

    def save(self, commit=True):
        user = super(Register_Form, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


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

    def __init__(self, *args, **kwargs):
        super(Login_Form, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password'].widget = forms.PasswordInput()


class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'city', 'user']


class CityPost_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class City_Form(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'state', 'country',
                  'photo_day', 'photo_night', 'population']
