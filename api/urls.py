from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from .views import FeedItemViewSet
from .views import ImageViewSet
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter(trailing_slash=False)
router.register('feed', FeedItemViewSet, basename='feed')
router.register('image', ImageViewSet, basename='image')

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = router.urls + [url('docs', schema_view)]