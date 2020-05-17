from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
import datetime
from project.helpers import RandomFileName

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    id = models.CharField('id', primary_key=True, max_length=255)
    is_authenticated = True

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class FeedItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)

class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to=RandomFileName('images'))
    feed_item = models.ForeignKey('api.FeedItem', blank=True, null=True, related_name='images', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url

class FeedItemComment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)
    feed_item = models.ForeignKey('api.FeedItem', blank=True, related_name='comments', on_delete=models.CASCADE)
