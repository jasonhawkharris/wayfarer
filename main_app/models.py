from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hometown = models.CharField(max_length=50)
    photo = models.CharField(
        max_length=250, default='images/default_profile.png')
    date_joined = datetime.date(datetime.now())

    def __str__(self):
        return self.user.username


# """ @receiver(post_save, sender=User)
# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         profile = Profile.objects.create(user=kwargs['instance'])

# post_save.connect(create_profile, sender=User) """


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    photo_day = models.CharField(max_length=250)
    photo_night = models.CharField(max_length=250, default='photo.jpg')
    population = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=40, default="No Title Provided")
    content = models.TextField(max_length=500)
    publish_date = datetime.date(datetime.now())
    city = models.ForeignKey(City,
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    publish_date = datetime.now()
    content = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
