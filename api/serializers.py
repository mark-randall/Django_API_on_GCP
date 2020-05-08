from rest_framework import serializers
from .models import FeedItem

class FeedItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    created = serializers.DateTimeField(read_only=True)