from rest_framework import serializers
from .models import FeedItem

class FeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItem
        fields = '__all__'