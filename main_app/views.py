from django.shortcuts import render, redirect
from .models import City, Profile

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import Login_Form, Profile_Form, UpdateProfile_Form, UpdateUser_Form, Register_Form
# Create your views here.


def home(request):
    login_modal = Login_Form()
    user_modal = Register_Form()
    #profile_modal = Profile_Form()
    context = {
        'login_form': login_modal,
        'user_form': user_modal,
        #'profile_form': profile_modal
    }
    return render(request, 'home.html', context)


def cities(request):
    my_cities = City.objects.all()
    login_modal = Login_Form()
    user_modal = Register_Form()
    context = {
        'cities': my_cities,
        'login_form': login_modal,
        'user_form': user_modal,
    }
    return render(request, 'cities.html', context)


""" def register(request):
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
    return render(request, 'home', context) """

def register(request):
    error_message = ''
    if request.method == 'POST':
        form = Register_Form(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.hometown = form.cleaned_data.get('hometown')
            user.profile.photo = form.cleaned_data.get('photo')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = Register_Form()
    return render(request, 'home', {'form': form})



def profile(request):
    error_message = ''
    if request.method == 'POST':
        updateU_form = UpdateUser_Form(request.POST, instance=request.user)
        updateP_form = UpdateProfile_Form(request.POST, instance=request.user.profile)
        if updateU_form.is_valid() and updateP_form.is_valid():
            updateU_form.save()
            updateP_form.save()
    else:
        updateP_form = UpdateProfile_Form()
        updateU_form = UpdateUser_Form()
    context = {
        'updateU_form': updateU_form,
        'updateP_form': updateP_form
    }
    return render(request, 'profile/profile_home.html', context)
