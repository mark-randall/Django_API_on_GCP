from rest_framework import serializers
from .models import FeedItem
from .models import Image

class FeedItemSerializer(serializers.ModelSerializer):
    image = serializers.StringRelatedField()

    class Meta:
        model = FeedItem
        fields = '__all__'
        ordering = ['created']

        

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        ordering = ['created']
