from django.db import models
import uuid
import datetime

class FeedItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
