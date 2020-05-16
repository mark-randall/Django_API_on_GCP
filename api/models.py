from django.db import models
import uuid
import datetime
from project.helpers import RandomFileName

class FeedItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)

class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to=RandomFileName('images'))
    feed_item = models.ForeignKey('api.FeedItem', blank=True, null=True, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url

class FeedItemComment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)
    feed_item = models.ForeignKey('api.FeedItem', blank=True, related_name='comments', on_delete=models.CASCADE)



