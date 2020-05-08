from django.urls import path
from rest_framework import routers
from .views import FeedItemViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('feed', FeedItemViewSet, basename='feed')
urlpatterns = router.urls