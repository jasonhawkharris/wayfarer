from django.shortcuts import render, redirect
from .models import City, Post, Profile
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import Login_Form, Profile_Form, UpdateProfile_Form, UpdateUser_Form, Register_Form
# Create your views here.


def home(request):
    login_modal = Login_Form()
    user_modal = Register_Form()
    cities = City.objects.all()
    context = {
        'login_form': login_modal,
        'user_form': user_modal,
        'cities': cities
    }
    return render(request, 'home.html', context)


def city_detail(request, city_id):
    city = City.objects.get(id=city_id)
    my_post = Post.objects.all()
    context = {
        'city': city,
        'posts': my_post
    }
    return render(request, 'cities/detail.html', context)


def cities(request):
    my_cities = City.objects.all()
    login_modal = Login_Form()
    user_modal = Register_Form()
    context = {
        'cities': my_cities,
        'login_form': login_modal,
        'user_form': user_modal,
    }
    return render(request, 'cities/index.html', context)


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
        updateP_form = UpdateProfile_Form(
            request.POST, instance=request.user.profile)
        if updateU_form.is_valid() and updateP_form.is_valid():
            updateU_form.save()
            updateP_form.save()
    else:
        updateP_form = UpdateProfile_Form()
        updateU_form = UpdateUser_Form()
    context = {
        'updateU_Form': updateU_form,
        'updateP_Form': updateP_form
    }
    return render(request, 'profile/profile_home.html', context)
