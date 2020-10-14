# ANCHOR External Modules
from django.http import request
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, ValidationError
from django.contrib.auth.decorators import login_required

# ANCHOR Internal Modules
from .models import City, Post, Profile
from .forms import *


# ANCHOR view functions
def home(request):
    login_modal = Login_Form()
    user_modal = Register_Form()
    all_posts = Post.objects.all()[:8]
    cities = City.objects.all()
    reroute = False
    context = {
        'login_form': login_modal,
        'user_form': user_modal,
        'all_posts': all_posts,
        'cities': cities,
        'reroute': reroute
    }
    return render(request, 'home.html', context)


# city: show
def city_detail(request, city_id):
    city = City.objects.get(id=city_id)
    my_post = Post.objects.all()
    context = {
        'city': city,
        'posts': my_post,
    }
    return render(request, 'cities/detail.html', context)


# post: create
@login_required
def add_post(request):
    if request.method == 'POST':
        user_id = User.objects.get(id=request.user.id)
        city_id = request.POST['city']
        city = City.objects.get(id=city_id)
        title = request.POST['title']
        content = request.POST['content']
        new_post = Post(title=title, content=content,
                        user=user_id, city=city)
        new_post.save()
    return redirect('profile', request.user.id)


# post: create/update
@login_required
def form(request):
    post_form = Post_Form()
    city_form = City_Form()
    my_cities = City.objects.all()
    context = {
        'post_form': post_form,
        'city_form': city_form,
        'cities': my_cities,
    }
    return render(request, 'posts/form.html',  context)


# cities: index
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


# post: index
@login_required
def posts(request):
    user_profile = Profile.objects.get(user=request.user.id)
    login_modal = Login_Form()
    user_modal = Register_Form()
    my_posts = Post.objects.all()
    context = {
        'posts': my_posts,
        'user_profile': user_profile,
        'login_form': login_modal,
        'user_form': user_modal
    }
    return render(request, 'posts/index.html', context)


# user posts: index
@login_required
def user_post_index(request, user_id):
    user_posts = Post.objects.filter(id=user_id)
    login_modal = Login_Form()
    user_modal = Register_Form()
    context = {
        'user_posts': user_posts,
        'login_form': login_modal,
        'user_form': user_modal
    }
    return render(request, 'profile/profile_home.html', context)


# post: show
def post(request, post_id):
    post = Post.objects.get(id=post_id)
    login_modal = Login_Form()
    user_modal = Register_Form()
    context = {
        'post': post,
        'login_form': login_modal,
        'user_form': user_modal
    }
    return render(request, 'posts/post.html', context)


# post edit
@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        edit_form = Post_Form(request.POST, instance=post)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('settings')
    else:
        login_modal = Login_Form()
        user_modal = Register_Form()
        edit_form = Post_Form(initial={
            'title': post.title,
            'content': post.content,
            'city': post.city,
            'user': request.user.id,
        })
        context = {
            'post': post,
            'edit_form': edit_form,
            'login_form': login_modal,
            'user_form': user_modal
        }
        return render(request, 'posts/edit.html', context)


# post: delete
@login_required
def post_delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect('profile', request.user.id)


# city posts: index
@login_required
def add_city_post(request, city_id):
    city = City.objects.get(id=city_id)
    if request.method == 'POST':
        post_form = CityPost_Form(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.city = city
            new_post.user = request.user
            new_post.save()
    return redirect('home')


# city: create
@login_required
def city_post_form(request, city_id):
    city = City.objects.get(id=city_id)
    city_name = city.name
    post_form = CityPost_Form()
    login_modal = Login_Form()
    user_modal = Register_Form()
    context = {
        'city': city,
        'city_name': city_name,
        'post_form': post_form,
        'login_form': login_modal,
        'user_form': user_modal
    }
    return render(request, 'cities/form.html', context)


# user: create
def register(request):
    error_message = 'this email is in use'
    if request.method == 'POST':
        form = Register_Form(request.POST)
        form_error = False
        if form.is_valid():
            form_error = False
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
            login_modal = Login_Form()
            user_modal = Register_Form()
            all_posts = Post.objects.all()[:8]
            cities = City.objects.all()
            reroute = True
            error_msg = 'Email or username was taken. Please try again.'
            context = {
                'login_form': login_modal,
                'user_form': user_modal,
                'all_posts': all_posts,
                'cities': cities,
                'reroute': reroute,
                'error_msg': error_msg
            }
            return render(request, 'home.html', context)


# posts/profile: update/delete
# profile: show
@login_required
def settings(request):
    error_message = ''
    if request.method == 'POST':
        updateU_form = UpdateUser_Form(request.POST, instance=request.user)
        updateP_form = UpdateProfile_Form(
            request.POST, instance=request.user.profile)
        if updateU_form.is_valid() and updateP_form.is_valid():
            updateU_form.save()
            updateP_form.save()
            return redirect('settings')
    else:
        user_posts = Post.objects.filter(user=request.user)
        login_modal = Login_Form()
        user_modal = Register_Form()
        updateP_form = UpdateProfile_Form(initial={
            'hometown': request.user.profile.hometown,
            'photo': request.user.profile.photo
        })
        updateU_form = UpdateUser_Form(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
            'email': request.user.email
        })
        context = {
            'updateU_form': updateU_form,
            'updateP_form': updateP_form,
            'user_posts': user_posts,
            'login_form': login_modal,
            'user_form': user_modal
        }
        return render(request, 'settings.html', context)


# profile show
@login_required
def profile(request, user_id):
    target_user = User.objects.get(id=user_id)
    login_modal = Login_Form()
    user_modal = Register_Form()
    user_profile = Profile.objects.get(user=user_id)
    user_posts = Post.objects.filter(user=user_id)
    context = {
        'target_user': target_user,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'login_form': login_modal,
        'user_form': user_modal
    }
    return render(request, 'profile/profile.html', context)


# redirects login from modal
def login_redirect(request):
    user = request.user
    return redirect('profile', user.id)


# city: create
@login_required
def add_city(request):
    if request.method == 'POST':
        city_form = City_Form(request.POST)
        if city_form.is_valid():
            new_city = city_form.save()
            return redirect('form')


# privacy: static
def privacy(request):
    login_modal = Login_Form()
    user_modal = Register_Form()
    context = {
        'login_form': login_modal,
        'user_form': user_modal
    }
    return render(request, 'privacy/privacy.html', context)
