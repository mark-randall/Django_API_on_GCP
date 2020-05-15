from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from .views import FeedItemViewSet
from .views import ImageViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register('feed', FeedItemViewSet, basename='feed')
router.register('image', ImageViewSet, basename='image')

urlpatterns = router.urls