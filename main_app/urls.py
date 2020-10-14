# ANCHOR External Modules
from django.urls import path

# ANCHOR Internal Modules
from . import views


# ANCHOR Urls
urlpatterns = [
    path('', views.home, name='home'),
    path('cities/', views.cities, name='cities'),
    path('cities/<int:city_id>/', views.city_detail, name='detail'),
    path('cities/<int:city_id>/add_city_post',
         views.add_city_post, name='add_city_post'),
    path('cities/<int:city_id>/city_post_form',
         views.city_post_form, name='city_post_form'),
    path('cities/add-city/', views.add_city, name='add_city'),
    path('posts/', views.posts, name='posts'),
    path('posts/form', views.form, name='form'),
    path('posts/add_post', views.add_post, name='add_post'),
    path('posts/<int:post_id>/', views.post, name='post'),
    path('post/<int:post_id>/edit', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('accounts/register/', views.register, name='register'),
    path('privacy/', views.privacy, name='privacy'),
]
