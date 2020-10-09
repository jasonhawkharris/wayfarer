from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('cities/', views.cities, name='cities'),
    path('cities/<int:city_id>/', views.city_detail, name='detail'),
    path('posts/', views.posts, name='posts'),
    path('accounts/register/', views.register, name='register'),
]
