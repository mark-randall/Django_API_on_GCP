from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import renderers
from api import helpers
from api import models
from api import serializers

class FeedItemViewSet(ModelViewSet):
    queryset = models.FeedItem.objects.all()
    serializer_class = serializers.FeedItemSerializer

class ImageViewSet(ModelViewSet):
    serializer_class = serializers.ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        feed_item_id = self.kwargs['feed_id']
        return models.Image.objects.filter(feed_item_id=feed_item_id)

class FeedItemCommentViewSet(ModelViewSet):
    serializer_class = serializers.FeedItemCommentSerializer

    def get_queryset(self):
        feed_item_id = self.kwargs['feed_id']
        return models.FeedItemComment.objects.filter(feed_item=feed_item_id)

