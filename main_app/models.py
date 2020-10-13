from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hometown = models.CharField(max_length=50)
    photo = models.CharField(max_length=250)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


@ receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=500)
    publish_date = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey(City,
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date']


class Comment(models.Model):
    publish_date = models.DateTimeField(
        default=timezone.now)
    content = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
