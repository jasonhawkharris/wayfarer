from django.shortcuts import render, redirect
from .models import City

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import Login_Form, User_Form, Profile_Form, UpdateProfile_Form
# Create your views here.


def home(request):
    login_modal = Login_Form()
    user_modal = User_Form()
    profile_modal = Profile_Form()
    context = {
        'login_form': login_modal,
        'user_form': user_modal,
        'profile_form': profile_modal
    }
    return render(request, 'home.html', context)


def cities(request):
    my_cities = City.objects.all()
    login_modal = Login_Form()
    user_modal = User_Form()
    profile_modal = Profile_Form()
    context = {
        'cities': my_cities,
        'login_form': login_modal,
        'user_form': user_modal,
        'profile_form': profile_modal
    }
    return render(request, 'cities.html', context)


def register(request):
    error_message = ''
    if request.method == 'POST':
        user_form = User_Form(request.POST)
        profile_form = Profile_Form(
            request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            return redirect('home')
    else:
        user_form = User_Form()
        profile_form = Profile_Form()
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'home', context)


def profile(request):
    error_message = ''
    if request.method == 'POST':
        update_form = UpdateProfile_Form(request.POST, instance=request.user.profile)
        if update_form.is_valid():
            update_form.save()
    else:
        update_form = UpdateProfile_Form()
    context = {
        'update_form': update_form
    }
    return render(request, 'profile/profile_home.html', context)
