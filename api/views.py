from http import HTTPStatus
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from .models import FeedItem
from .serializers import FeedItemSerializer

class FeedItemViewSet(ViewSet):

    def list(self, request):
        queryset = [FeedItem()]
        serializer = FeedItemSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def retrieve(self, request, pk=None):
        return JsonResponse(status=HTTPStatus.NOT_FOUND, data={'status': 'false', 'message': 'not found'})

