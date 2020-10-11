from main_app.views import add_post, add_city_post
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('cities/', views.cities, name='cities'),
    path('cities/<int:city_id>/', views.city_detail, name='detail'),
    path('posts/add_post', views.add_post, name='add_post'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:post_id>/', views.post, name='post'),
    path('posts/form', views.form, name='form'),
    path('accounts/register/', views.register, name='register'),
    path('cities/<int:city_id>/add_city_post', views.add_city_post, name='add_city_post'),
    path('cities/<int:city_id>/city_post_form', views.city_post_form, name='city_post_form'),
]
