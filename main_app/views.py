from django.shortcuts import render, redirect
from .models import City, Post, Profile
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import Login_Form, Profile_Form, UpdateProfile_Form, UpdateUser_Form, Register_Form, Post_Form
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
        'posts': my_post,
    }

    return render(request, 'cities/detail.html', context)


def add_post(request):
    if request.method == 'POST':
        post_form = Post_Form(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.save()
    return redirect('form')


def form(request):
    post_form = Post_Form()
    my_cities = City.objects.all()
    context = {
        'post_form': post_form,
        'cities': my_cities,
    }
    return render(request, 'posts/form.html',  context)


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


def posts(request):
    user_profile = Profile.objects.get(user=request.user.id)
    my_posts = Post.objects.all()
    context = {'posts': my_posts, 'user_profile':user_profile}
    return render(request, 'posts/index.html', context)


def post(request, post_id):
    post = Post.objects.get(id=post_id)
    
    context = {'post': post}
    return render(request, 'posts/post.html', context)


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


def settings(request):
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
        'updateU_form': updateU_form,
        'updateP_form': updateP_form
    }
    return render(request, 'settings.html', context)


def profile(request):
    user_profile = Profile.objects.get(user=request.user.id)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile/profile.html', context)
