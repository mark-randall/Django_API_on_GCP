from django.db import models
import uuid
import datetime
from project.helpers import RandomFileName

class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to=RandomFileName('images'))

    def __str__(self):
        return self.image.url

class FeedItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE)



