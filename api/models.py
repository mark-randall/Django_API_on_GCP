from django.db import models
import uuid
import datetime

class FeedItem:
    id = uuid.uuid4()
    created = datetime.datetime.now()
    title = 'test'
