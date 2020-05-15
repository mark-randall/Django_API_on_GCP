from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import renderers
from .models import FeedItem
from .serializers import FeedItemSerializer
from .models import Image
from .serializers import ImageSerializer

class FeedItemViewSet(ModelViewSet):
    queryset = FeedItem.objects.all()
    serializer_class = FeedItemSerializer

class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser,)

