from django.http import request
from django.shortcuts import render, redirect
from .models import City, Post, Profile
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import Login_Form, Profile_Form, UpdateProfile_Form, UpdateUser_Form, Register_Form, Post_Form, CityPost_Form, City_Form
from django.utils import timezone
# Create your views here.


def home(request):
    login_modal = Login_Form()
    user_modal = Register_Form()
    all_posts = Post.objects.all()[:5]
    cities = City.objects.all()
    context = {
        'login_form': login_modal,
        'user_form': user_modal,
        'all_posts': all_posts,
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
        # post_form = Post_Form(request.POST)
        user_id = User.objects.get(id=request.user.id)
        city_id = request.POST['city']
        city = City.objects.get(id=city_id)
        title = request.POST['title']
        content = request.POST['content']
        new_post = Post(title=title, content=content,
                        user=user_id, city=city)
        new_post.save()
    return redirect('home')


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
    context = {'posts': my_posts, 'user_profile': user_profile}
    return render(request, 'posts/index.html', context)


def user_post_index(request, user_id):
    user_posts = Post.objects.filter(id=user_id)
    context = {'user_posts': user_posts}
    return render(request, 'profile/profile_home.html', context)


def post(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'posts/post.html', context)

# def edit(request, post_id):
#     post = Post.objects.get(id=post_id)
#     edit_form = Post_Form(request.POST, instance=post)
#     context = {'post': post, 'edit_form':edit_form}
#     return render(request, 'posts/edit.html', context)


def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        edit_form = Post_Form(request.POST, instance=post)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('settings')
    else:
        edit_form = Post_Form(initial={
            'title': post.title,
            'content': post.content,
            'city': post.city,
            'user': request.user.id,
        })
        context = {
            'post': post,
            'edit_form': edit_form
        }
        return render(request, 'posts/edit.html', context)


def post_delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect("settings")


# post for specific city page


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


def city_post_form(request, city_id):
    city = City.objects.get(id=city_id)
    city_name = city.name
    post_form = CityPost_Form()
    context = {'city': city, 'city_name': city_name, 'post_form': post_form}
    return render(request, 'cities/form.html', context)


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
            # user.profile.photo = form.cleaned_data.get('photo')
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
        user_posts = Post.objects.filter(user=request.user)
        updateP_form = UpdateProfile_Form()
        updateU_form = UpdateUser_Form()
    context = {
        'updateU_form': updateU_form,
        'updateP_form': updateP_form,
        'user_posts': user_posts
    }
    return render(request, 'settings.html', context)


def profile(request, user_id):
    target_user = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user_id)
    user_posts = Post.objects.filter(user=user_id)
    context = {
        'target_user': target_user,
        'user_profile': user_profile,
        'user_posts': user_posts
    }
    return render(request, 'profile/profile.html', context)


def login_redirect(request):
    user = request.user
    return redirect('profile', user.id)


def add_city(request):
    if request.method == 'POST':
        city_form = City_Form(request.POST)
        if city_form.is_valid():
            new_city = city_form.save()
            return redirect('form')
