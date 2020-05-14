from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import FeedItem
from .serializers import FeedItemSerializer

class FeedItemViewSet(ModelViewSet):
    queryset = FeedItem.objects.all()
    serializer_class = FeedItemSerializer

