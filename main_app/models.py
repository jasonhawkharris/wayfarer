# ANCHOR External modules
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Requires that each new email and username be unique
User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True


# ANCHOR Models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hometown = models.CharField(max_length=50)
    photo = models.CharField(max_length=250)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


@ receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    """
    update_profile_signal: Allows Profile model to 
    communicate with User model
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class City(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(null=True)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    photo_day = models.CharField(max_length=250)
    photo_night = models.CharField(max_length=250, default='photo.jpg')
    population = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=500)
    publish_date = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey(City,
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title


class Comment(models.Model):
    publish_date = models.DateTimeField(
        default=timezone.now)
    content = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
