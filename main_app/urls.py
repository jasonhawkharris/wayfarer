from main_app.views import add_post
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('cities/', views.cities, name='cities'),
    path('cities/<int:city_id>/', views.city_detail, name='detail'),
    path('posts/add_post', views.add_post, name='add_post'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:post_id>/', views.post, name='post'),
    path('posts/form', views.form, name='form'),
    # path('post/<int:post_id>/edit', views.edit, name='edit'),
    path('accounts/register/', views.register, name='register'),
]
