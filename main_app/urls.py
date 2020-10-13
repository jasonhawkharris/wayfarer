from main_app.views import add_post, add_city_post
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('cities/', views.cities, name='cities'),
    path('cities/<int:city_id>/', views.city_detail, name='detail'),
    path('posts/add_post', views.add_post, name='add_post'),
    path('posts/', views.posts, name='posts'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:post_id>/', views.post, name='post'),
    path('posts/form', views.form, name='form'),
    path('post/<int:post_id>/edit', views.edit_post, name='edit_post'),
    path('accounts/register/', views.register, name='register'),
    path('cities/<int:city_id>/add_city_post',
         views.add_city_post, name='add_city_post'),
    path('cities/<int:city_id>/city_post_form',
         views.city_post_form, name='city_post_form'),
    path('cities/add-city/', views.add_city, name='add_city'),
    path('privacy/', views.privacy, name='privacy'),
]
